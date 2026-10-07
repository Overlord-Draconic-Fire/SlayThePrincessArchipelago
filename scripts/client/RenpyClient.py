from __future__ import annotations

from asyncio import AbstractEventLoop
import logging
import typing
import Utils
import renpy

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

    def has_location(self, location_name: str) -> bool:
            """Return True if the player has sent this location to the server."""
            location_lookup: typing.Mapping[int, str] = self.location_names[self.game]
            location_id: int | None = next((location_id for location_id, resolved_name in location_lookup.items() if resolved_name == location_name), None)
            if location_id is None:
                return False
            return location_id in self.checked_locations

    def count_item(self, item_name: str) -> int:
        """Count how many instances of an item name the player owns."""
        item_lookup: typing.Mapping[int, str] = self.item_names[self.game]
        item_id: int | None = next((item_id for item_id, resolved_name in item_lookup.items() if resolved_name == item_name), None)
        if item_id is None:
            return 0
        return sum(1 for net_item in self.items_received if net_item.item == item_id)

    def can_access_region(self, region_name: str) -> bool:
        from REGION_REQUIREMENTS import REGION_REQUIREMENTS as RR
        from TrackerSystem import REGION_TO_ENTRANCES as RE, get_bladeless_name, get_blade_name_for_region

        # Check if we already know the region_name
        region_access = set(Utils.persistent_load().get(self.slot_key, {}).get("region_access", []))
        if region_name in region_access:
            return True

        # Check REGION_REQUIREMENTS to know all necessary items
        requirements = RR.get(region_name, None)
        if requirements is not None:
            if self.check_requirements(requirements) and self.can_pass_entrance(region_name):
                self.inform_access_region(region_name)
                return True
            return False
        
        # Not in REGION_REQUIREMENTS, go check REGION_TO_ENTRANCES because it's a main chap 3 region
        region_bladeless_name = get_bladeless_name(region_name)
        if region_bladeless_name != region_name and not renpy.store.hasThisBlade(get_blade_name_for_region(region_name)):
            return False  # On doit avoir la Blade

        region_to_entrance = RE.get(region_bladeless_name, None)
        if region_to_entrance is not None:
            for sub_region in region_to_entrance:
                if self.can_access_region(sub_region):
                    self.inform_access_region(region_name)
                    return True # Just need one accessible sub region
            return False

        # Error, Region unknow
        self._notify(f"Region not found: {region_name}", "error")
        return False

    def check_requirements(self, requirements: list) -> bool:
        for required_item in requirements:
            if "Princess -" in required_item and self.get_chapter_access() in [0, 2]:
                continue
            if "Voice -" in required_item and self.get_chapter_access() in [0, 1]:
                continue
            if "Pristine" in required_item and renpy.store.hasThisBlade(required_item):
                continue

            if not self.has_item(required_item):
                renpy.store.last_region_failed_requirement = required_item
                return False
        return True

    def can_pass_entrance(self, region_name: str):
        from TrackerSystem import RANDO_ENTRANCE, ENTRANCE_REQUIREMENT, get_bladeless_name

        new_entrance = RANDO_ENTRANCE.get(get_bladeless_name(region_name))
        if new_entrance is None:
            return True

        return self.can_access_region(ENTRANCE_REQUIREMENT[new_entrance])

    def inform_access_region(self, region_name: str) -> None:
        region_access = set(Utils.persistent_load().get(self.slot_key, {}).get("region_access", []))
        region_access.add(region_name)
        Utils.persistent_store(self.slot_key, "region_access", list(region_access))

    def can_access_function(self, function_name: str, number: int) -> bool:
        """Check if player can access a function based on owned princesses and voices."""

        function_access = Utils.persistent_load().get(self.slot_key, {}).get(function_name, 0)
        return function_access >= number

    def inform_access_function(self, function_name: str, number: int) -> None:
        function_access = Utils.persistent_load().get(self.slot_key, {}).get(function_name, 0)
        function_access = max(function_access, number)
        Utils.persistent_store(self.slot_key, function_name, function_access)

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

        # Check if already sent to server
        if location_id in self.checked_locations:
            return False

        self.locations_checked.add(location_id)

        loop = self.loop
        if loop is None or loop.is_closed():
            self._notify(f"Cannot send location: inactive event loop ({location_name})", "error")
            return False

        if self.autoreconnect_task is not None:
            self._notify(f"Location queued for server: '{location_name}' ({location_id})", "debug")
            return False

        import asyncio
        try:
            asyncio.run_coroutine_threadsafe(self.check_locations([location_id]), loop)
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

    def get_goal(self) -> int:
        return self.get_slot_option_int("goal")

    def get_memories_hunt(self) -> int:
        return self.get_slot_option_int("memories_hunt")

    def get_deathlink(self) -> int:
        return self.get_slot_option_int("death_link")

    def get_chapter_access(self) -> int:
        return self.get_slot_option_int("chapter_access")

    def get_pristine_blade_rando(self) -> int:
        return self.get_slot_option_int("pristine_blade_rando")

    def get_pristine_sword_rando(self) -> bool:
        return self.get_slot_option_bool("pristine_sword_rando")

    def get_narrator_rando(self) -> bool:
        return self.get_slot_option_bool("narrator_rando")

    def get_save_slot_rando(self) -> int:
            return self.get_slot_option_int("save_slot_rando", -1)
    
    def get_gift_rando(self) -> int:
            return self.get_slot_option_int("gift_rando")

    def get_memoriesanity(self) -> int:
            return self.get_slot_option_int("memoriesanity")

    def get_chapter_rando(self) -> int:
        return self.get_slot_option_int("chapter_rando")

    def get_voice_rando(self) -> bool:
        return self.get_slot_option_bool("voice_rando")

    def get_heart_rando(self) -> int:
        return self.get_slot_option_int("heart_rando")

    def get_mirror_rando(self) -> int:
        return self.get_slot_option_int("mirror_rando")

    def get_oblivion_rando(self) -> bool:
        return self.get_slot_option_bool("oblivion_rando")

    def item_received(self, net_item: NetworkItem) -> None:
        """Notify Ren'Py when this client actually receives an item."""
        try:
            item_name: str = self.item_names.lookup_in_slot(net_item.item, self.slot)

            item_callback = getattr(self, "on_item_received_callback", None)
            if item_callback is not None:
                item_callback(item_name)

            renpy.store.galleryInitializer.refresh_all_location_access()
        except Exception:
            logger.exception("item_received callback failed")

    def cmd_received(self, args: dict) -> None:
        def escape_notify_text(text: str) -> str:
            return text.replace("{", "{{").replace("}", "}}")

        try:
            if args["cmd"] == "PrintJSON":
                type_arg = args.get("type")
                if type_arg is None:
                    self._notify(escape_notify_text(str(args["data"][0]["text"])), "server")
                elif type_arg == "Chat":
                    self._notify(escape_notify_text(str(args["data"][0]["text"])), "player")
                elif type_arg == "ServerChat":
                    self._notify(escape_notify_text(str(args["data"][0]["text"][10:])), "server")
                elif type_arg in ["CommandResult", "Join", "TagsChanged", "Tutorial"]:
                    self._notify(escape_notify_text(str(args["data"][0]["text"])), "ap")
                elif type_arg == "ItemSend":
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
