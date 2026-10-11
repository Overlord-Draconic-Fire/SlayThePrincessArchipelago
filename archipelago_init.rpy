if True:
    define config.developer = True
    define config.autoreload = False
    define config.console = True
    define config.rollback_enabled = True

default last_region_checked = None
default last_region_failed_requirement = None
default ap_console_command = ""
default contrarian_choices_remaining = 0
default trap_queue = []
default stubborn_texts = ["[[Slay the Princess", "[[Take the blade", "[[Retrieve the blade", "[[Destroy her", "[[Hurl the blade at her eye",
"[[Make her suffer with you", "[[Fight back", "[[Turn back", "[[Attack her", "[[Drop her", "[[Finish the job", "[[Round three", "[[Go out fighting", 
"[[Rush for the blade", "[[Unlodge the blade", "[[Pick up the blade", "[[Keep pushing", "[[Keep pushing", "[[Keep pushing", "[[Grab the Princess"]
default smitten_texts = ["[[Save the Princess", "[[Drop the blade", "[[Give her", "[[Throw the blade", "[[Toss your weapon", "[[Offer her your hand",
"[[Embrace your new goddess", "[[Suffer", "[[Submit", "[[Cut her free", "[[Do it. Toss the blade", "[[Warn her", "[[Resist", "[[Sit with them", "[[Fight back",
"[[Rescue the Princess", "[[You're not doing that", "[[Sit with her", "[[Break her chains", "[[Kiss her", "[[Examine the chains"]

init -10 python:
    import os
    import sys
    from collections import deque
    
    # Paths to Add
    base_dir = os.path.join(renpy.config.basedir, "game")
    paths_to_add = [
        os.path.join(base_dir, "scripts", "client", "dependencies"),
        os.path.join(base_dir, "scripts", "client"),
        os.path.join(base_dir, "scripts", "help"),
        base_dir
    ]
    for path in paths_to_add:
        if path not in sys.path:
            sys.path.insert(0, path)
    
    # Import modules
    import enum
    import Utils
    import threading
    import websockets

    import Location
    import Item
    import Region

    store._deathlink_event = threading.Event()
    store._ap_text_queue = deque()
    store.gallery_lock = threading.Lock()

    class ConsoleArchipelago:
        ap_console_messages: list[dict[str, str]] = []
    console = ConsoleArchipelago()

    def _ap_process_pending_text() -> bool:
        while store._ap_text_queue:
            msg_str, level_key = store._ap_text_queue.popleft()
            _ap_notify_mainthread(msg_str, level_key)
        return False

    def _ap_process_pending_deathlink() -> bool:
        if store._deathlink_event.is_set():
            store._deathlink_event.clear()
            renpy.call_in_new_context("deathlink")
        return False

    _trap_labels = {
        Item.heroTrap: "trap_hero",
        Item.huntedTrap: "trap_hunted",
        Item.paranoidTrap: "trap_paranoid",
    }
    _trap_events = {item: threading.Event() for item in _trap_labels}

    def _ap_process_pending_traps() -> bool:
        for item, event in _trap_events.items():
            if event.is_set():
                event.clear()
                renpy.call_in_new_context(_trap_labels[item])
                return False

        return False

    if _ap_process_pending_text not in renpy.config.periodic_callbacks:
        renpy.config.periodic_callbacks.append(_ap_process_pending_text)
    if _ap_process_pending_deathlink not in renpy.config.periodic_callbacks:
        renpy.config.periodic_callbacks.append(_ap_process_pending_deathlink)
    if _ap_process_pending_traps not in renpy.config.periodic_callbacks:
        renpy.config.periodic_callbacks.append(_ap_process_pending_traps)

    def ap_console_force_bottom():
        store.ap_console_scroll_bottom = False

        if store.ap_console_scroll:
            store.ap_console_scroll.value = store.ap_console_scroll.range

    def ap_console_append_message(message: str, level_key: str) -> str:
        full_message = f"[{level_key.upper()}] {message}"
        console.ap_console_messages.append({"level": level_key, "text": str(full_message)})

        if len(console.ap_console_messages) > 250:
            del console.ap_console_messages[: len(console.ap_console_messages) - 250]

        store.ap_console_scroll_bottom = True
        renpy.restart_interaction()

        return full_message

    def ap_console_open() -> None:
        renpy.show_screen("ap_console")
        renpy.restart_interaction()

    def ap_console_close() -> None:
        renpy.hide_screen("ap_console")
        renpy.restart_interaction()

    def ap_console_submit() -> None:
        message = str(store.ap_console_command or "").strip()
        store.ap_console_command = ""
        if not message:
            return
        
        try:
            if getattr(archipelago, "loop", None) and not archipelago.loop.is_closed():
                import asyncio
                asyncio.run_coroutine_threadsafe(
                    archipelago.send_msgs([{"cmd": "Say", "text": message}]),
                    archipelago.loop,
                )
        except Exception as exc:
            ap_console_append_message(f"Send failed: {exc}", "error")

    def voice_character(voice_name, **kwargs):
        location_name = voice_name.replace("of the", "Introduction - The")
        kwargs["callback"] = lambda event, **callback_kwargs: voice_callback(location_name, event, **callback_kwargs)
        return Character(voice_name, **kwargs)

    class ConnectionState(enum.Enum):
        DISCONNECTED = enum.auto()
        CONNECTING = enum.auto()
        AUTOCONNECTING = enum.auto()
        CONNECTED = enum.auto()
        DISCONNECTING = enum.auto()

    # Store client and lock in a shared container for thread-safe access
    class ArchipelagoManager:
        def __init__(self):
            self._client = None
            self.lock = threading.Lock()
            self.state = ConnectionState.DISCONNECTED

        @property
        def connecting(self) -> bool:
            with self.lock:
                return self.state == ConnectionState.CONNECTING

        @property
        def stopping(self) -> bool:
            with self.lock:
                return self.state == ConnectionState.DISCONNECTING

        @property
        def autoconnecting(self) -> bool:
            with self.lock:
                return self.state == ConnectionState.AUTOCONNECTING

        def set_state(self, state: ConnectionState) -> None:
            with self.lock:
                self.state = state
            ap_notify_renpy()

        def set_client(self, client: RenpyContext) -> None:
            """Thread-safe update of archipelago client."""
            with self.lock:
                self._client = client

        def get_client(self) -> Optional[RenpyContext]:
            with self.lock:
                return self._client

        def is_current_client(self, client: RenpyContext) -> bool:
            with self.lock:
                return self._client is client

        def clear_client(self, client: RenpyContext) -> bool:
            """Clear the client only if it is still the active client."""
            with self.lock:
                if self._client is not client:
                    return False

                self._client = None

            self.set_state(ConnectionState.DISCONNECTED)
            return True
        
        
        def __getattr__(self, name):
            try:
                with self.lock:
                    if self._client is None:
                        def dummy(*args, inform_player=True, **kwargs):
                            if inform_player:
                                ap_error("Archipelago not initialized")
                            return None
                        return dummy

                    return getattr(self._client, name)
            except Exception:
                def dummy(*args, inform_player=True, **kwargs):
                    if inform_player:
                        import traceback
                        ap_error(f"error whith the function {name}")
                        traceback.print_exc()
                    return None
                return dummy
    
    # Global instance
    archipelago = ArchipelagoManager()

    def _ap_notify_mainthread(message: str, level_key: str) -> None:
        full_message = ap_console_append_message(message, level_key)

        if level_key not in ["debug", "ap"]:
            safe_message = message.replace("{", "{{").replace("}", "}}")
            renpy.notify(safe_message)
        print(full_message)

    def ap_notify(message: str, level: str = "level missing") -> None:
        if level == "AUTO":
            archipelago.set_state(ConnectionState.AUTOCONNECTING)
            return

        msg_str = str(message)
        level_key = str(level).lower().strip()

        store._ap_text_queue.append((msg_str, level_key))

        if threading.current_thread() is not threading.main_thread() and renpy.display.interface is not None:
            renpy.display.interface.post_time_event()

    def ap_notify_renpy() -> None:
        if threading.current_thread() is not threading.main_thread():
            if renpy.display.interface is not None:
                renpy.display.interface.post_time_event()
        else:
            renpy.restart_interaction()

    def ap_debug(message: str) -> None:
        ap_notify(message, "debug")

    def ap_error(message: str) -> None:
        ap_notify(message, "error")

    def ap_info(message: str) -> None:
        ap_notify(message, "info")

    def voice_callback(location_name, event, **kwargs):
        if event != "show":
            return

        send_location(location_name, group="Voice")

    def send_location(location_name : str, location2 : str = None, group : str = None) -> None:
        """Send an arbitrary location check."""
        if "Find" in location_name and not archipelago.get_chapter_rando() in [1, 3]:
            return
        elif "Reach" in location_name and not archipelago.get_chapter_rando() in [2, 3]:
            return
        elif "Heart" in location_name and archipelago.get_heart_rando() == 0:
            return
        elif group == "Voice" and archipelago.get_voice_rando() == 0:
            return
        elif group == "Blade" and archipelago.get_location_blade_rando() == 0:
            return
        elif group == "MirrorSB" and not archipelago.get_mirror_rando() in [1, 3]:
            return
        elif group == "MirrorChap" and not archipelago.get_mirror_rando() in [2, 3]:
            return
        elif group == "Oblivion" and not archipelago.get_oblivion_rando():
            return
        elif group == "Gift" and not archipelago.get_gift_rando() in [1, 3]:
            return

        if location2 != None and archipelago.get_heart_rando() == 2:
            archipelago.send_location(location2)
        else:
            archipelago.send_location(location_name)

    def hasThisBlade(blade_value : str) -> bool:
        """
        Check whether the player has a blade.
        Accepts an item value like Item.blade_wild and returns True if:
        - The player has the specific blade, OR
        - The player has the chapter blade (blade3 for chapter 3), OR
        - The player has the global blade (blade)
        """
        # Check specific blade
        if archipelago.has_item(blade_value):
            return True
        
        # Check chapter-specific blade
        import BLADE_CHAPTER_MAP
        if blade_value in BLADE_CHAPTER_MAP.BLADE_CHAPTER_MAP:
            chapter = BLADE_CHAPTER_MAP.BLADE_CHAPTER_MAP[blade_value]
            chapter_blade = f"blade{chapter}"
            chapter_item = getattr(Item, chapter_blade)
            if archipelago.has_item(chapter_item):
                return True
        
        # Check global blade
        if archipelago.has_item(Item.blade):
            return True

        if blade_value == Item.sword:
            return not archipelago.get_pristine_sword_rando()
        
        return archipelago.get_pristine_blade_rando() == 0

    def hasVoice(voice_value : str) -> bool:
        """
        Check whether the player has the specified voice.
        """

        return archipelago.get_chapter_access() in [0, 1] or archipelago.has_item(voice_value)

    def hasItem(item_value : str) -> bool:
        """
        Check whether the player has the specified item.
        Accepts an item value like Item.narrator and returns True if the player has that item.
        """

        have = archipelago.has_item(item_value)
        if have:
            ap_debug(f"Player have {item_value}")
        else:
            ap_debug(f"Player does not have {item_value}")
        return have

    def hasXItem(item_value : str, x : int) -> bool:
        """
        Check whether the player has at least x of the specified item.
        Accepts an item value like Item.heart and returns True if the player has at least x of that item.
        """
        store.last_region_checked = None
        if item_value == Item.invitation:
            store.last_region_checked = Region.space_between

        store.last_region_failed_requirement = None

        count = archipelago.count_item(item_value)
        ap_debug(f"Player has {count} of {item_value} (needs {x})")
        if count < x:
            store.last_region_failed_requirement = f"{x - count} {item_value}"
        return count >= x

    def hasRegionRequirements(region_value : str) -> bool: #DEBUG TOUT REMPLACER PAR archipelago.can_access_region !
        """
        Check whether the player has all required items for a region.
        The parameter must be a region value (e.g., Region.needle_hunted).
        """
        try:
            store.last_region_checked = region_value
            return archipelago.can_access_region(region_value)
        except Exception as e:
            ap_error(f"Error in hasRegionRequirements({region_value}): {e}")
            return False

    def send_deathlink(message: str, type_death: bool) -> None:
        """Send a deathlink to the Archipelago server."""
        try:
            deathlink = archipelago.get_deathlink()

            if deathlink in (0, 1) or deathlink == {True: 2, False: 3}[type_death]:
                return

            import asyncio
            message = message.replace("[player_name]", archipelago.player_names[archipelago.slot])
            asyncio.run_coroutine_threadsafe(archipelago.send_death(message), archipelago.loop)
            ap_debug(f"DeathLink sent: {message}")
        except Exception as e:
            ap_error(f"Error while sending DeathLink '{message}': {e}")

    def instante_kill() -> None:
        ap_debug("DeathLink applied")
        store._deathlink_event.set()
        if renpy.display.interface is not None:
            renpy.display.interface.post_time_event()

    def unlock_gallery() -> None:
        route_groups = [
            globals().get("routesParent", []),
            globals().get("altRoutesParent", []),
            globals().get("routesParentLower", []),
        ]

        for group in route_groups:
            for route in group:
                route.unlock_gallery()

    def _build_gallery_route_map():
        route_map = {}

        route_groups = [
            globals().get("routesParent", []),
            globals().get("altRoutesParent", []),
            globals().get("routesParentLower", []),
        ]

        for group in route_groups:
            for route in group:
                # route.routeName = _("The Stranger")
                route_map[str(route.routeName)] = route

        return route_map

    def _parse_ap_gallery_name(name: str):
        try:
            base, index = name.rsplit(f" [", 1)
            base = base[10:] # remove "Gallery - "
            index = int(index[:-1])  # remove "]"
            return base, index
        except Exception as e:
            ap_error(f"Error in _parse_ap_gallery_name(): {e}")
            import traceback        
            traceback.print_exc()
            return None, None

    def ap_handle_received_item(item_name: str) -> None:
        """Handle AP item reception hooks, unlock gallery items or play trap when received from the server."""
        try:
            if "Gallery" not in item_name:
                if "Trap of The" in item_name:
                    ap_handle_trap(item_name)
                return

            route_name, index = _parse_ap_gallery_name(item_name)
            if not route_name:
                return

            route_map = _build_gallery_route_map()
            route = route_map.get(route_name)

            if route is None:
                ap_error(f"Unknown gallery route: {route_name}")
                return

            # sécurité index
            if index < 1 or index > len(route.items):
                ap_error(f"Invalid index {index} for {route_name}")
                return

            route.unlock_item(index, checkAchievement=True, from_server=True)
        except Exception as e:
            ap_error(f"Error in ap_handle_received_item({item_name}): {e}")
            import traceback        
            traceback.print_exc()

    def ap_handle_trap(item_name: str) -> None:
        ap_debug(item_name)
        if item_name == Item.brokenTrap:
            broken_start_sobbing()
        elif item_name == Item.contrarianTrap:
            store.contrarian_choices_remaining += 3
        elif item_name == Item.stubbornTrap:
            store.trap_queue.append("stubborn")
        elif item_name == Item.smittenTrap:
            store.trap_queue.append("smitten")
        elif item_name in _trap_events:
            _trap_events[item_name].set()
        if renpy.display.interface is not None:
            renpy.display.interface.post_time_event()

    def force_trap_choice(items):
        stubborn_indices = []
        smitten_indices = []

        for index, item in enumerate(items):
            caption = item.caption.lower()

            if any(text.lower() in caption for text in store.stubborn_texts):
                stubborn_indices.append(index)

            if any(text.lower() in caption for text in store.smitten_texts):
                smitten_indices.append(index)

        for trap_index, trap in enumerate(store.trap_queue):
            if trap == "stubborn" and stubborn_indices:
                store.trap_queue.pop(trap_index)
                return stubborn_indices

            if trap == "smitten" and smitten_indices:
                store.trap_queue.pop(trap_index)
                return smitten_indices

        return []

    def contrarian_prepare_choices(items):
        displayed_items = [
            [item.caption, item.action]
            for item in items
        ]

        if store.contrarian_choices_remaining <= 0:
            return displayed_items

        actionable_indices = [
            index
            for index, item in enumerate(displayed_items)
            if item[1] is not None
        ]


        if len(actionable_indices) < 2:
            return displayed_items

        ap_debug("Contrarian Trap applied")

        shuffled_actions = [
            displayed_items[index][1]
            for index in actionable_indices
        ]

        import random
        random.shuffle(shuffled_actions)

        for index, action in zip(actionable_indices, shuffled_actions):
            displayed_items[index][1] = action

        store.contrarian_choices_remaining -= 1
        ap_debug(f"Contrarian Trap remaining {store.contrarian_choices_remaining}")

        return displayed_items

    def broken_start_sobbing():
        renpy.music.play("audio/voices/ch3/fury/broken/fury_broken_sob.flac", channel="broken_sobbing", loop=True)

    def broken_stop_sobbing():
        renpy.music.stop(channel="broken_sobbing", fadeout=1.0)