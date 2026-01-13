from __future__ import annotations

import logging
import typing

from CommunClient import CommonContext, NetworkItem

logger = logging.getLogger("Client")


class RenpyContext(CommonContext):
    """Context for embedding AP in Ren'Py without a GUI or text UI."""

    # Receive all items: 1 (basic) + 2 (remote) + 4 (remote start)
    tags = CommonContext.tags | {"AP"}
    items_handling = 0b111
    want_slot_data = True

    async def server_auth(self, password_requested: bool = False):
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
        item_id = self.item_names[self.game].get(item_name)
        if item_id is None:
            return False
        return any(net_item.item == item_id for net_item in self.items_received)

    def count_item(self, item_name: str) -> int:
        """Count how many instances of an item name the player owns."""
        item_id = self.item_names[self.game].get(item_name)
        if item_id is None:
            return 0
        return sum(1 for net_item in self.items_received if net_item.item == item_id)

    def can_access_region(self, region_name: str) -> bool:
        """Check if player can access a region based on owned princesses and voices."""
        
        from REGION_REQUIREMENTS import REGION_REQUIREMENTS

        required_items = REGION_REQUIREMENTS.get(region_name)
        if required_items is None:
            logger.warning(f"Unknown region: {region_name}")
            return False

        for item in required_items:
            if not self.has_item(item):
                return False
        return True

    def send_location(self, location_name: str) -> bool:
        """Send a location check to Archipelago if it hasn't been checked yet."""
        # Look up the location ID from the game's location names
        location_id = self.location_names[self.game].get(location_name)
        if location_id is None:
            logger.warning(f"Unknown location: {location_name}")
            return False
        
        # Check if already sent
        if location_id in self.checked_locations:
            logger.info(f"Location {location_name} already checked")
            return False
        
        # Send the location check
        import asyncio
        asyncio.create_task(self.check_locations([location_id]))
        logger.info(f"Sent location check for: {location_name}")
        return True

    def item_received(self, net_item: NetworkItem) -> None:
        """Notify Ren'Py when this client actually receives an item."""
        if self.on_text_callback:
            try:
                item_name = self.item_names.lookup_in_slot(net_item.item, self.slot)
                sender = self.player_names.get(net_item.player, str(net_item.player))
                self.on_text_callback(f"Reçu: {item_name} (de {sender})")
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
) -> CommonContext:
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
