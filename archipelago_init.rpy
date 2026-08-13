if True:
    define config.developer = True
    define config.autoreload = False
    define config.console = True
    define config.rollback_enabled = True

default ap_console_command = ""

init:
    # Archipelago characters
    define ap = Character("Archipelago", color = "#ffffff", what_color = "#ffffff", what_text_align=0.5, what_outlines=[ (3, "#000000") ], who_outlines= [ (3, "#000000") ], what_style = "voice_style", ctc="ctc_blink", ctc_position="nestled")

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
    import Utils
    import threading
    import asyncio
    import websockets

    import Location
    import GalleryLocation
    import Item
    import Region
    import BLADE_CHAPTER_MAP
    import REGION_REQUIREMENTS

    store.last_region_checked = None  # Global variable tracking the last region checked
    store.last_region_failed_requirement = None  # Global variable tracking the failed requirements in the last region checked
    store.Location = Location
    store.GalleryLocation = GalleryLocation
    store.Item = Item
    store.Region = Region
    store.BLADE_CHAPTER_MAP = BLADE_CHAPTER_MAP
    store._deathlink_event = threading.Event()
    store._ap_text_queue = deque()
    store.gallery_lock = threading.Lock()
    store.ap_console_command = ""

    class ConsoleArchipelago:
        ap_console_messages: list[dict[str, str]] = []
    console = ConsoleArchipelago()

    def _ap_process_pending_deathlink() -> bool:
        if store._deathlink_event.is_set():
            store._deathlink_event.clear()
            renpy.call_in_new_context("deathlink")
        return False

    def _ap_process_pending_text() -> bool:
        while store._ap_text_queue:
            msg_str, level_key = store._ap_text_queue.popleft()
            _ap_notify_mainthread(msg_str, level_key)
        return False

    if _ap_process_pending_deathlink not in renpy.config.periodic_callbacks:
        renpy.config.periodic_callbacks.append(_ap_process_pending_deathlink)
    if _ap_process_pending_text not in renpy.config.periodic_callbacks:
        renpy.config.periodic_callbacks.append(_ap_process_pending_text)

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

    # Store client and lock in a shared container for thread-safe access
    class ArchipelagoManager:
        def __init__(self):
            self.client = None
            self.lock = threading.Lock()
            self.connecting = False
            self.stopping = False

        def set_client(self, client: RenpyContext) -> None:
            """Thread-safe update of archipelago client."""
            with self.lock:
                self.client = client
                if client:
                    try:
                        client.on_item_received_callback = ap_handle_received_item
                        renpy.restart_interaction()
                    except Exception:
                        import traceback
                        ap_error("error with on_item_received_callback")
                        traceback.print_exc()
        
        def __getattr__(self, name):
            try:
                with self.lock:
                    if self.client is None:
                        ap_error("Archipelago not initialized")
                        return

                    return getattr(self.client, name)
            except Exception:
                import traceback
                ap_error(f"error whith the function {name}")
                traceback.print_exc()
    
    # Global instance
    archipelago = ArchipelagoManager()

    def _ap_notify_mainthread(message: str, level_key: str) -> None:
        full_message = ap_console_append_message(message, level_key)

        if level_key not in ["debug", "ap"]:
            safe_message = message.replace("{", "{{").replace("}", "}}")
            renpy.notify(safe_message)
        print(full_message)

    def ap_notify(message: str, level: str = "level missing") -> None:
        msg_str = str(message)
        level_key = str(level).lower().strip()

        store._ap_text_queue.append((msg_str, level_key))

        if threading.current_thread() is not threading.main_thread() and renpy.display.interface is not None:
            renpy.display.interface.post_time_event()

    def ap_debug(message: str) -> None:
        ap_notify(message, "debug")

    def ap_error(message: str) -> None:
        ap_notify(message, "error")

    def ap_info(message: str) -> None:
        ap_notify(message, "info")

    def send_location(location_name : str, location2 : str = None, group : str = None) -> None:
        """Send an arbitrary location check."""
        if "Find" in location_name and not archipelago.get_chapter_rando() in [1, 3]:
            return
        elif "Reach" in location_name and not archipelago.get_chapter_rando() in [2, 3]:
            return
        elif "Heart" in location_name and archipelago.get_heart_rando() == 0:
            return
        elif group == "Mirror" and not archipelago.get_mirror_rando():
            return
        elif group == "Oblivion" and not archipelago.get_oblivion_rando():
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
            ap_debug(f"Player has specific blade: {blade_value}")
            return True
        
        # Check chapter-specific blade
        if blade_value in BLADE_CHAPTER_MAP.BLADE_CHAPTER_MAP:
            chapter = BLADE_CHAPTER_MAP.BLADE_CHAPTER_MAP[blade_value]
            chapter_blade = f"blade{chapter}"
            chapter_item = getattr(Item, chapter_blade)
            if archipelago.has_item(chapter_item):
                ap_debug(f"Player has chapter blade: {chapter_item}")
                return True
        
        # Check global blade
        if archipelago.has_item(Item.blade):
            ap_debug(f"Player has global blade: {Item.blade}")
            return True

        if blade_value == Item.sword:
            return not archipelago.get_pristine_sword_rando()
        
        return archipelago.get_pristine_blade_rando() == 0

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
        if item_value == Item.gift:
            store.last_region_checked = Region.space_between

        store.last_region_failed_requirement = None

        count = archipelago.count_item(item_value)
        ap_debug(f"Player has {count} of {item_value} (needs {x})")
        if count < x:
            store.last_region_failed_requirement = f"{x - count} {item_value}"
        return count >= x

    def hasRegionRequirements(region_value : str) -> bool:
        """
        Check whether the player has all required items for a region.
        The parameter must be a region value (e.g., Region.needle_hunted).
        """
        try:
            store.last_region_checked = region_value
            store.last_region_failed_requirement = None

            requirements = REGION_REQUIREMENTS.REGION_REQUIREMENTS.get(region_value)
            if not requirements:
                ap_error(f"No requirements found for region: {region_value}")
                return False

            for required_item in requirements:
                if not archipelago.get_chapter_access() in [1, 3] and "(Princess)" in required_item:
                    continue
                if not archipelago.get_chapter_access() in [2, 3] and "(Voice)" in required_item:
                    continue

                if not archipelago.has_item(required_item):
                    store.last_region_failed_requirement = required_item
                    return False

            return True
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

    def check_for_memories() -> None:
        if archipelago.get_memoriesanity() == 0:
            return
        
        route_groups = [
            globals().get("routesParent", []),
            globals().get("altRoutesParent", []),
            globals().get("routesParentLower", []),
        ]

        for group in route_groups:
            for route in group:
                route.unlock_gallery()
                for item in route.items:
                    route.lock_item(item.itemNumber)

        lst = Utils.persistent_load().get("gallery", {}).get(archipelago.slot_key, [])
        for image in lst:
            ap_handle_received_item(image)

        renpy.save_persistent()

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

    def ap_gallery_unlock_all() -> bool:
        try:
            route_groups = [
                globals().get("routesParent", []),
                globals().get("altRoutesParent", []),
                globals().get("routesParentLower", []),
            ]

            for group in route_groups:
                for route in group:
                    route.unlock_gallery()
                    for item in route.items:
                        route.unlock_item(item.itemNumber, checkAchievement=False, from_server=True)

            if "galleryAchievementChecker" in globals():
                galleryAchievementChecker.checkAchievement()

            renpy.save_persistent()
            ap_debug("Gallery updated: full unlock applied.")
            return True
        except Exception as e:
            ap_error(f"Error in ap_gallery_unlock_all(): {e}")
            import traceback        
            traceback.print_exc()
            return False

    def ap_handle_received_item(item_name: str) -> None:
        """Handle AP item reception hooks and unlock gallery items when received from the server."""
        try:
            if "Gallery" not in item_name:
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

            route.unlock_gallery()
            route.unlock_item(index, checkAchievement=True, from_server=True)

            renpy.save_persistent()
        except Exception as e:
            ap_error(f"Error in ap_handle_received_item({item_name}): {e}")
            import traceback        
            traceback.print_exc()

label chapter_requirements_failed:
    $ send_deathlink("[player_name] does not have the necessary items", False)
    $ ap_debug(f"{store.last_region_checked}: missing {store.last_region_failed_requirement}")
    ap "The time for this meeting has not yet come. Return when fate allows your paths to cross."
    menu:
        ap "Your story cannot continue from here."

        "{i}• [[Return to the main menu.]]{/i}":
            $ renpy.full_restart()
    return

label no_chose_left:
    $ send_deathlink("[player_name] cannot make a choice.", False)
    $ ap_debug("No choices left")
    $ config.menu_include_disabled = True
    menu:
        ap "Your story cannot continue from here."

        "{i}• [[Maybe something was forgotten.]{/i}" if False:
            pass

        "{i}• [[Maybe somewhere else awaits first.]{/i}" if False:
            pass

        "{i}• [[Maybe this is not the right time.]{/i}" if False:
            pass

        "{i}• [[Return when fate allows it.]{/i}" if False:
            pass

        "{i}• [[Return to the main menu.]]{/i}":
            $ config.menu_include_disabled = False
            $ renpy.full_restart()
    return

label deathlink:
    ap "Another soul has fallen. Fate demands you do the same."
    $ renpy.full_restart()