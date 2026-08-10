from __future__ import annotations

from asyncio import AbstractEventLoop
import logging
import typing

from CommunClient import CommonContext, NetworkItem
from NetUtils import ClientStatus

logger: logging.Logger = logging.getLogger("Client")


class RenpyContext(CommonContext):
    """Context for embedding AP in Ren'Py without a GUI or text UI."""

    # Receive all items: 1 (basic) + 2 (remote) + 4 (remote start)
    tags: typing.Set[str] = CommonContext.tags | {"AP"}
    items_handling = 0b111
    want_slot_data = True

    trying_to_connect: bool = False
    ap_console_messages: list[dict[str, str]] = []

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
            self._notify(f"Unknown location: '{location_name}'", "error")
            return False

        # Check if already sent to server (from any previous session or this one)
        if location_id in self.checked_locations:
            self._notify(f"Location already sent: '{location_name}' ({location_id})", "debug")
            return False

        # Send the location check on the background event loop
        if not self.loop or self.loop.is_closed():
            self._notify(f"Cannot send location: inactive event loop ({location_name})", "error")
            return False

        import asyncio
        try:
            asyncio.run_coroutine_threadsafe(self.check_locations([location_id]), self.loop)
            self._notify(f"Location sent: '{location_name}' ({location_id})", "debug")
            return True
        except Exception:
            logger.exception("send_location failed")
            self._notify(f"Error while sending location '{location_name}'", "error")
            return False

    def send_goal(self) -> bool:
        """Mark this slot as goal-complete on the Archipelago server."""
        if not self.loop or self.loop.is_closed():
            self._notify("Cannot send goal: inactive event loop", "error")
            return False

        import asyncio
        try:
            self.finished_game = True
            asyncio.run_coroutine_threadsafe(
                self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}]),
                self.loop,
            ).result(timeout=2.0)
            self._notify("Goal status sent", "debug")
            return True
        except Exception:
            self._notify("Error while sending goal status", "error")
            return False

    def get_slot_option(self, key: str, default: typing.Any = None) -> typing.Any:
        data = getattr(self, "slot_data", {}) or {}
        return data.get(key, default)

    def get_slot_option_bool(self, key: str, default: bool = False) -> bool:
        value = self.get_slot_option(key, default)
        if isinstance(value, str):
            lowered = value.strip().lower()
            if lowered in {"1", "true", "yes", "on"}:
                return True
            if lowered in {"0", "false", "no", "off", ""}:
                return False
        return bool(value)

    def get_slot_option_int(self, key: str, default: int = 0) -> int:
        value = self.get_slot_option(key, default)
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    def get_deathlink(self) -> int:
        return self.get_slot_option_int("death_link", 0)

    def get_chapter_access(self) -> int:
        return self.get_slot_option_int("chapter_access", 4)

    def get_pristine_blade_rando(self) -> int:
        return self.get_slot_option_int("pristine_blade_rando", 2)

    def get_pristine_sword_rando(self) -> bool:
        return self.get_slot_option_bool("pristine_sword_rando", True)

    def get_gift_rando(self) -> bool:
        return self.get_slot_option_bool("gift_rando", True)

    def get_narrator_rando(self) -> bool:
        return self.get_slot_option_bool("narrator_rando", True)

    def get_chapter_rando(self) -> int:
        return self.get_slot_option_int("chapter_rando", 3)

    def get_heart_rando(self) -> int:
        return self.get_slot_option_int("heart_rando", 1)

    def get_mirror_rando(self) -> bool:
        return self.get_slot_option_bool("mirror_rando", True)

    def get_oblivion_rando(self) -> bool:
        return self.get_slot_option_bool("oblivion_rando", True)

    def get_memoriesanity(self) -> int:
        return self.get_slot_option_int("memoriesanity", 0)

    def _notify(self, message: str, level: str) -> None:
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
                callback(message, level)
            elif self.loop and self.loop.is_running():
                self.loop.call_soon_threadsafe(callback, message, level)
            else:
                callback(message, level)
        except Exception:
            logger.exception("_notify failed")

    def item_received(self, net_item: NetworkItem) -> None:
        """Notify Ren'Py when this client actually receives an item."""
        try:
            item_name: str = self.item_names.lookup_in_slot(net_item.item, self.slot)

            item_callback = getattr(self, "on_item_received_callback", None)
            if item_callback is not None:
                item_callback(item_name)
        except Exception:
            logger.exception("item_received callback failed")

    def cmd_received(self, args: dict) -> None:
        def escape_notify_text(text: str) -> str:
            return text.replace("{", "{{").replace("}", "}}")

        try:
            if args["cmd"] == "PrintJSON":
                if args["type"] == "Chat":
                    self._notify(escape_notify_text(str(args["data"][0]["text"])), "player")
                elif args["type"] == "ServerChat":
                    self._notify(escape_notify_text(str(args["data"][0]["text"][10:])), "server")
                elif args["type"] in ["CommandResult", "Join", "TagsChanged", "Tutorial"]:
                    self._notify(escape_notify_text(str(args["data"][0]["text"])), "ap")
                elif args["type"] == "ItemSend":
                    self.item_sent(args["data"])
        except Exception:
            logger.exception("cmd_received failed")

    def item_sent(self, data: list) -> None:
        result = []
        for part in data:
            part_type = part.get("type")

            if part_type == "player_id":
                player_id = int(part["text"])
                result.append(self.player_names.get(player_id, str(player_id)))
            elif part_type == "item_id":
                object_id = int(part["text"])
                player_id = part.get("player")
                result.append(self.item_names.lookup_in_slot(object_id, player_id))
            elif part_type == "location_id":
                object_id = int(part["text"])
                player_id = part.get("player")
                result.append(self.location_names.lookup_in_slot(object_id, player_id))
            else:
                result.append(part.get("text", ""))

        message = "".join(result)
        self._notify(str(message), "ap")

    async def want_deathlink(self) -> None:
        """Request DeathLink support from the server if the slot allows it."""
        if self.get_deathlink() > 0:
            import asyncio
            try:
                await self.update_death_link(True)
                self._notify("DeathLink requested", "debug")
            except Exception:
                self._notify("Error while requesting DeathLink", "error")

    def on_deathlink(self, data: typing.Dict[str, typing.Any]) -> None:
        """Gets dispatched when a new DeathLink is triggered by another linked player."""
        self.last_death_link = max(data["time"], self.last_death_link)
        text = data.get("cause", "")
        if text:
            self._notify(f"DeathLink: {text}", "ap")
        else:
            self._notify(f"DeathLink: Received from {data['source']}", "ap")

        try:
            if self.on_kill_callback:
                self.on_kill_callback()
        except Exception:
            logger.exception("DeathLink label jump failed")

def create_renpy_client(server_address: str, slot_name: str, password: typing.Optional[str] = None, *,
    tags: typing.Optional[typing.Iterable[str]] = None, on_text: typing.Optional[typing.Callable[[str], None]] = None,
    on_json: typing.Optional[typing.Callable[[typing.Any], None]] = None, on_kill: typing.Optional[typing.Callable[[], None]] = None) -> RenpyContext:

    ctx = RenpyContext(server_address, password)
    ctx.username = slot_name
    ctx.auth = slot_name
    ctx.items_handling = 0b111  # Ensure items_handling is set
    ctx.game = "Slay The Princess"
    if tags:
        ctx.tags |= set(tags)
    ctx.on_text_callback = on_text
    ctx.on_json_callback = on_json
    ctx.on_kill_callback = on_kill
    return ctx
