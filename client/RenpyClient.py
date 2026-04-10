from __future__ import annotations

from asyncio import AbstractEventLoop
import logging
import typing

from CommunClient import CommonContext, NetworkItem

logger: logging.Logger = logging.getLogger("Client")


class RenpyContext(CommonContext):
    """Context for embedding AP in Ren'Py without a GUI or text UI."""

    # Receive all items: 1 (basic) + 2 (remote) + 4 (remote start)
    tags: typing.Set[str] = CommonContext.tags | {"AP"}
    items_handling = 0b111
    want_slot_data = True

    async def server_auth(self, password_requested: bool = False) -> None:
        """Send Connect packet when server is ready, matching the protocol."""
        logger.info(f"[RenpyContext.server_auth] Called with password_requested={password_requested}")
        if password_requested and not self.password:
            # No console input available in Ren'Py; abort if password was not provided by the caller.
            logger.error("Password required but not provided; aborting connection.")
            self.disconnected_intentionally = True
            if self.server and self.server.socket:
                await self.server.socket.close()
            return
        if not self.auth:
            self.auth = self.username
        logger.info(
            f"[RenpyContext.server_auth] Sending Connect with slot: {self.auth}, game: {self.game}, "
            f"items_handling: {self.items_handling}"
        )
        await self.send_connect()
        logger.info("[RenpyContext.server_auth] Connect sent")

    def has_item(self, item_name: str) -> bool:
        """Return True if the player owns at least one instance of the given item name."""
        item_lookup: typing.Mapping[int, str] = self.item_names[self.game]
        item_id: int | None = next((item_id for item_id, resolved_name in item_lookup.items() if resolved_name == item_name), None)
        if item_id is None:
            return False
        return any(net_item.item == item_id for net_item in self.items_received)

    def count_item(self, item_name: str) -> int:
        """Count how many instances of an item name the player owns."""
        item_lookup: typing.Mapping[int, str] = self.item_names[self.game]
        item_id: int | None = next((item_id for item_id, resolved_name in item_lookup.items() if resolved_name == item_name), None)
        if item_id is None:
            return 0
        return sum(1 for net_item in self.items_received if net_item.item == item_id)

    def can_access_region(self, region_name: str) -> bool:
        """Check if player can access a region based on owned princesses and voices."""
        
        from REGION_REQUIREMENTS import REGION_REQUIREMENTS

        required_items: list[str] | None = REGION_REQUIREMENTS.get(region_name)
        if required_items is None:
            logger.warning(f"Unknown region: {region_name}")
            return False

        for item in required_items:
            if not self.has_item(item):
                return False
        return True

    def send_location(self, location_name: str) -> bool:
        """Send a location check to Archipelago if it hasn't been checked yet."""
        # Look up the location ID from the game's location names (id -> name mapping)
        location_map: typing.Mapping[int, str] = self.location_names[self.game]
        norm_target: str = str(location_name).strip().lower()

        # Build a normalized reverse map once per call (safe: map is small)
        normalized_reverse: dict[str, int] = {str(name).strip().lower(): lid for lid, name in location_map.items()}
        location_id: int | None = normalized_reverse.get(norm_target)

        if location_id is None:
            self._notify(f"Unknown location: '{location_name}'")
            return False

        # Check if already sent to server (from any previous session or this one)
        if location_id in self.checked_locations:
            self._notify(f"Location already sent: '{location_name}' ({location_id})")
            return False

        # Send the location check on the background event loop
        if not self.loop or self.loop.is_closed():
            self._notify(f"Cannot send location: inactive event loop ({location_name})")
            return False

        import asyncio
        try:
            asyncio.run_coroutine_threadsafe(self.check_locations([location_id]), self.loop)
            self._notify(f"Location sent: '{location_name}' ({location_id})")
            return True
        except Exception:
            logger.exception("send_location failed")
            self._notify(f"Error while sending location '{location_name}'")
            return False

    def _notify(self, message: str) -> None:
        """Thread-safe bridge to on_text_callback (ap_notify)."""
        logger.info(message)
        
        callback: typing.Any | None = getattr(self, "on_text_callback", None)
        if not callback:
            return

        try:
            import asyncio
            # If we're already on the stored loop, call directly; otherwise, schedule thread-safely.
            try:
                running_loop: AbstractEventLoop = asyncio.get_running_loop()
            except RuntimeError:
                running_loop = None

            if self.loop and running_loop and running_loop is self.loop:
                callback(message)
            elif self.loop and self.loop.is_running():
                self.loop.call_soon_threadsafe(callback, message)
            else:
                callback(message)
        except Exception:
            logger.exception("_notify failed")


    def item_received(self, net_item: NetworkItem) -> None:
        """Notify Ren'Py when this client actually receives an item."""
        if self.on_text_callback:
            try:
                item_name: str = self.item_names.lookup_in_slot(net_item.item, self.slot)
                sender: str = self.player_names.get(net_item.player, str(net_item.player))
                self.on_text_callback(f"Received: {item_name} ({sender})")
            except Exception:
                logger.exception("item_received callback failed")


def create_renpy_client(
    server_address: str,
    slot_name: str,
    password: typing.Optional[str] = None,
    *,
    tags: typing.Optional[typing.Iterable[str]] = None,
    on_text: typing.Optional[typing.Callable[[str], None]] = None,
    on_json: typing.Optional[typing.Callable[[typing.Any], None]] = None,
) -> RenpyContext:
    """Factory for embedding the client in non-text hosts (e.g., Ren'Py).

    Connection is not started automatically; call ctx.connect() then await ctx.message_loop().
    """
    ctx = RenpyContext(server_address, password)
    ctx.username = slot_name
    ctx.auth = slot_name
    ctx.items_handling = 0b111  # Ensure items_handling is set
    ctx.game = "Slay The Princess"
    if tags:
        ctx.tags |= set(tags)
    ctx.on_text_callback = on_text
    ctx.on_json_callback = on_json
    return ctx
