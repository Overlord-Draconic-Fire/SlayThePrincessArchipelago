if True:
    define config.developer = True
    define config.autoreload = False
    define config.console = True
    define config.rollback_enabled = True


init -10 python:
    import os
    import sys
    
    # Force the correct absolute path
    base_dir = os.path.join(renpy.config.basedir, "game")
    
    # Paths to add in priority order
    paths_to_add = [
        os.path.join(base_dir, "client", "dependencies"),
        os.path.join(base_dir, "client"),
        os.path.join(base_dir, "help"),
        base_dir
    ]
    
    # Add ALL paths
    for path in paths_to_add:
        if path not in sys.path:
            sys.path.insert(0, path)
    
    # Import modules
    import Utils
    import threading
    import asyncio
    import websockets

    import Location
    import Item
    import Region
    import DAGGER_CHAPTER_MAP
    import REGION_REQUIREMENTS

    store.last_region_checked = None  # Global variable tracking the last region checked
    store.last_region_failed_requirement = None  # Global variable tracking the failed requirements in the last region checked
    store.Location = Location
    store.Item = Item
    store.Region = Region
    store.DAGGER_CHAPTER_MAP = DAGGER_CHAPTER_MAP
    
    # Store client and lock in a shared container for thread-safe access
    class ArchipelagoManager:
        def __init__(self):
            self.client = None
            self.lock = threading.Lock()
        
        def get_client(self):
            """Thread-safe access to archipelago_client from any thread."""
            with self.lock:
                return self.client
        
        def set_client(self, client):
            """Thread-safe update of archipelago_client."""
            with self.lock:
                self.client = client
    
    # Global instance
    archipelago = ArchipelagoManager()

    def ap_notify(message, level: str = "debug") -> None:
        """
        Unified AP notification helper.
        - level="debug": console/dev only, prefixed with [DEBUG]
        - level="ap": player-facing only, prefixed with [AP]
        - level="info": both console and player, prefixed with [INFO]
        """
        msg_str = str(message)
        level_key = str(level).lower().strip()

        if level_key not in ("debug", "ap", "info"):
            level_key = "debug"

        prefix_map = {
            "debug": "[DEBUG]",
            "ap": "[AP]",
            "info": "[INFO]",
        }
        full_message = f"{prefix_map[level_key]} {msg_str}"

        renpy.notify(msg_str)
        print(full_message)

    def ap_debug(message) -> None:
        ap_notify(message, "debug")

    def ap_player(message) -> None:
        ap_notify(message, "ap")

    def ap_info(message) -> None:
        ap_notify(message, "info")

    def get_archipelago_client() -> RenpyContext:
        """Thread-safe access to archipelago_client from any thread."""
        return archipelago.get_client()
    
    def set_archipelago_client(client: RenpyContext) -> None:
        """Thread-safe update of archipelago_client."""
        archipelago.set_client(client)
        try:
            renpy.restart_interaction()
        except Exception:
            pass

    def send_location(location_name : str) -> None:
        """Send an arbitrary location check."""
        try:
            client : RenpyContext = get_archipelago_client()
            if client:
                if "Find" in location_name and not get_chapter_rando():
                    return
                if "Reach" in location_name and not get_global_chapter_rando():
                    return
                if "Heart" in location_name and not get_heart_rando():
                    return

                client.send_location(location_name)
            else:
                ap_info("archipelago not initialized")
        except Exception as e:
            import traceback
            ap_debug(f"Error while sending location: {e}")
            traceback.print_exc()

    def send_goal() -> None:
        """Mark current AP slot as having completed its goal."""
        try:
            client : RenpyContext = get_archipelago_client()
            if client:
                client.send_goal()
            else:
                ap_info("archipelago not initialized")
        except Exception as e:
            import traceback
            ap_debug(f"Error while sending goal status: {e}")
            traceback.print_exc()

    def get_slot_data() -> dict:
        """Return AP slot_data for this player (empty dict if unavailable)."""
        try:
            client : RenpyContext = get_archipelago_client()
            if client:
                return client.get_slot_data()
        except Exception as e:
            ap_debug(f"Error in get_slot_data(): {e}")
        return {}

    def get_slot_option_bool(key: str, default: bool = False) -> bool:
        """Read a boolean option from AP slot_data."""
        try:
            client : RenpyContext = get_archipelago_client()
            if client:
                return client.get_slot_option_bool(key, default)
        except Exception as e:
            ap_debug(f"Error in get_slot_option_bool({key}): {e}")
        return default

    def get_slot_option_int(key: str, default: int = 0) -> int:
        """Read an integer option from AP slot_data."""
        try:
            client : RenpyContext = get_archipelago_client()
            if client:
                return client.get_slot_option_int(key, default)
        except Exception as e:
            ap_debug(f"Error in get_slot_option_int({key}): {e}")
        return default

    def get_chapter_access() -> int:
        """Read slot_data['chapter_access']."""
        try:
            client : RenpyContext = get_archipelago_client()
            if client:
                return client.get_chapter_access()
        except Exception as e:
            ap_debug(f"Error in get_chapter_access(): {e}")
        return ChapterAccessRando.default

    def get_pristine_dagger_rando() -> int:
        """Read slot_data['pristine_dagger_rando']."""
        try:
            client : RenpyContext = get_archipelago_client()
            if client:
                return client.get_pristine_dagger_rando()
        except Exception as e:
            ap_debug(f"Error in get_pristine_dagger_rando(): {e}")
        return PristineDaggerRando.default

    def get_gift_rando() -> bool:
        """Read slot_data['gift_rando']."""
        try:
            client : RenpyContext = get_archipelago_client()
            if client:
                return client.get_gift_rando()
        except Exception as e:
            ap_debug(f"Error in get_gift_rando(): {e}")
        return False

    def get_chapter_rando() -> bool:
        """Read slot_data['chapter_rando']."""
        try:
            client : RenpyContext = get_archipelago_client()
            if client:
                return client.get_chapter_rando()
        except Exception as e:
            ap_debug(f"Error in get_chapter_rando(): {e}")
        return False

    def get_global_chapter_rando() -> bool:
        """Read slot_data['global_chapter_rando']."""
        try:
            client : RenpyContext = get_archipelago_client()
            if client:
                return client.get_global_chapter_rando()
        except Exception as e:
            ap_debug(f"Error in get_global_chapter_rando(): {e}")
        return False

    def get_heart_rando() -> bool:
        """Read slot_data['heart_rando']."""
        try:
            client : RenpyContext = get_archipelago_client()
            if client:
                return client.get_heart_rando()
        except Exception as e:
            ap_debug(f"Error in get_heart_rando(): {e}")
        return False

    def get_mirror_rando() -> bool:
        """Read slot_data['mirror_rando']."""
        try:
            client : RenpyContext = get_archipelago_client()
            if client:
                return client.get_mirror_rando()
        except Exception as e:
            ap_debug(f"Error in get_mirror_rando(): {e}")
        return False

    def hasThisDagger(dagger_value : str) -> bool:
        """
        Check whether the player has a dagger.
        Accepts an item value like Item.dagger_wild and returns True if:
        - The player has the specific dagger, OR
        - The player has the chapter dagger (dagger3 for chapter 3), OR
        - The player has the global dagger (dagger)
        """
        try:
            client : RenpyContext = get_archipelago_client()
            if not client:
                ap_info("archipelago not initialized")
                return False

            # Check specific dagger
            if client.has_item(dagger_value):
                ap_debug(f"Player has specific dagger: {dagger_value}")
                return True
            
            # Check chapter-specific dagger
            if dagger_value in DAGGER_CHAPTER_MAP.DAGGER_CHAPTER_MAP:
                chapter = DAGGER_CHAPTER_MAP.DAGGER_CHAPTER_MAP[dagger_value]
                chapter_dagger = f"dagger{chapter}"
                chapter_item = getattr(Item, chapter_dagger)
                if client.has_item(chapter_item):
                    ap_debug(f"Player has chapter dagger: {chapter_item}")
                    return True
            
            # Check global dagger
            if client.has_item(Item.dagger):
                ap_debug(f"Player has global dagger: {Item.dagger}")
                return True
            
            return get_pristine_dagger_rando() == 0
        except Exception as e:
            ap_debug(f"Error in hasThisDagger({dagger_value}): {e}")
            return False

    def hasXItem(item_value : str, x : int) -> bool:
        """
        Check whether the player has at least x of the specified item.
        Accepts an item value like Item.heart and returns True if the player has at least x of that item.
        """
        try:
            store.last_region_checked = None
            if item_value == Item.gift:
                store.last_region_checked = Region.space_between

            store.last_region_failed_requirement = None

            client : RenpyContext = get_archipelago_client()
            if not client:
                ap_info("archipelago not initialized")
                return False

            count = client.count_item(item_value)
            ap_debug(f"Player has {count} of {item_value} (needs {x})")
            if count < x:
                store.last_region_failed_requirement = (x - count) + " " + item_value
            return count >= x
        except Exception as e:
            ap_debug(f"Error in hasXItem({item_value}, {x}): {e}")
            return False

    def hasRegionRequirements(region_value : str) -> bool:
        """
        Check whether the player has all required items for a region.
        The parameter must be a region value (e.g., Region.needle_hunted).
        """
        try:
            store.last_region_checked = region_value
            store.last_region_failed_requirement = None

            client : RenpyContext = get_archipelago_client()
            if not client:
                return False

            requirements = REGION_REQUIREMENTS.REGION_REQUIREMENTS.get(region_value)
            if not requirements:
                ap_debug(f"No requirements found for region: {region_value}")
                return False

            for required_item in requirements:
                if not get_chapter_access() in [1, 3] and "(Princess)" in required_item:
                    continue
                if not get_chapter_access() in [2, 3] and "(Voice)" in required_item:
                    continue

                if not client.has_item(required_item):
                    store.last_region_failed_requirement = required_item
                    return False

            return True
        except Exception as e:
            ap_debug(f"Error in hasRegionRequirements({region_value}): {e}")
            return False



label chapter_requirements_failed:
    $ ap_info(f"{store.last_region_checked}: missing {store.last_region_failed_requirement}")
    ap "The time for this meeting has not yet come. Return when fate allows your paths to cross."
    menu:
        "Return to the main menu.":
            $ renpy.full_restart()
    return