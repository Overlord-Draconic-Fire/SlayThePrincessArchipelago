if True:
    define config.developer = True
    define config.autoreload = False
    define config.console = True
    define config.rollback_enabled = True

init:
    # Archipelago characters
    define ap = Character("Archipelago", color = "#ffffff", what_color = "#ffffff", what_text_align=0.5, what_outlines=[ (3, "#000000") ], who_outlines= [ (3, "#000000") ], what_style = "voice_style", ctc="ctc_blink", ctc_position="nestled")

init 1 python:
    if get_memoriesanity():
        ap_gallery_lock_images()

init -10 python:
    import os
    import sys
    
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
        if client:
            try:
                client.on_item_received_callback = ap_handle_received_item
            except Exception:
                pass
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

    def get_pristine_blade_rando() -> int:
        """Read slot_data['pristine_blade_rando']."""
        try:
            client : RenpyContext = get_archipelago_client()
            if client:
                return client.get_pristine_blade_rando()
        except Exception as e:
            ap_debug(f"Error in get_pristine_blade_rando(): {e}")
        return PristineBladeRando.default

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

    def get_memoriesanity() -> int:
        """Read slot_data['memoriesanity']."""
        try:
            client : RenpyContext = get_archipelago_client()
            if client:
                return client.get_memoriesanity()
        except Exception as e:
            ap_debug(f"Error in get_memoriesanity(): {e}")
        return 0

    def hasThisBlade(blade_value : str) -> bool:
        """
        Check whether the player has a blade.
        Accepts an item value like Item.blade_wild and returns True if:
        - The player has the specific blade, OR
        - The player has the chapter blade (blade3 for chapter 3), OR
        - The player has the global blade (blade)
        """
        try:
            client : RenpyContext = get_archipelago_client()
            if not client:
                ap_info("archipelago not initialized")
                return False

            # Check specific blade
            if client.has_item(blade_value):
                ap_debug(f"Player has specific blade: {blade_value}")
                return True
            
            # Check chapter-specific blade
            if blade_value in BLADE_CHAPTER_MAP.BLADE_CHAPTER_MAP:
                chapter = BLADE_CHAPTER_MAP.BLADE_CHAPTER_MAP[blade_value]
                chapter_blade = f"blade{chapter}"
                chapter_item = getattr(Item, chapter_blade)
                if client.has_item(chapter_item):
                    ap_debug(f"Player has chapter blade: {chapter_item}")
                    return True
            
            # Check global blade
            if client.has_item(Item.blade):
                ap_debug(f"Player has global blade: {Item.blade}")
                return True
            
            return get_pristine_blade_rando() == 0
        except Exception as e:
            ap_debug(f"Error in hasThisBlade({blade_value}): {e}")
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

    def _get_gallery_item_numbers(route) -> list:
        """Return every item index for a gallery route, even if items are not initialized yet."""
        try:
            if hasattr(route, "items") and route.items:
                return [item.itemNumber for item in route.items]

            length = int(getattr(route, "imagesLength", 0))
            if length > 0:
                return list(range(1, length + 1))
        except Exception:
            pass

        return []

    def _gallery_list_name_from_route_key(route_key: str) -> str:
        route_map = {
            "zch1": "princess",
            "ztlq": "spaceBetween",
            "zfinale": "finale",
        }
        return route_map.get(route_key, route_key)

    def _gallery_route_key_from_list_name(list_name: str) -> str:
        list_map = {
            "princess": "zch1",
            "spaceBetween": "ztlq",
            "finale": "zfinale",
        }
        return list_map.get(list_name, list_name)

    def get_gallery_location_name(route_key: str, index: int) -> str:
        """Resolve the AP location string for one gallery image by route key + 1-based index."""
        try:
            list_name = _gallery_list_name_from_route_key(str(route_key))
            gallery_list = getattr(GalleryLocation, list_name, None)
            item_index = int(index)
            if isinstance(gallery_list, list) and 0 < item_index < len(gallery_list):
                return gallery_list[item_index]
        except Exception as e:
            ap_debug(f"Error in get_gallery_location_name({route_key}, {index}): {e}")
        return ""

    def _resolve_gallery_item_from_name(item_name: str):
        """Return (route_key, index) for a gallery AP item/location name, else None."""
        try:
            target = str(item_name).strip().lower()
            for list_name in dir(GalleryLocation):
                if list_name.startswith("_"):
                    continue
                values = getattr(GalleryLocation, list_name, None)
                if not isinstance(values, list):
                    continue
                for idx in range(1, len(values)):
                    if str(values[idx]).strip().lower() == target:
                        return (_gallery_route_key_from_list_name(list_name), idx)
        except Exception as e:
            ap_debug(f"Error in _resolve_gallery_item_from_name({item_name}): {e}")
        return None

    def _get_gallery_route_by_key(route_key: str):
        return globals().get(f"gallery_{route_key}")

    def ap_unlock_gallery_item_from_name(item_name: str, unlock_route: bool = True) -> bool:
        """Unlock a single gallery image from an AP item/location display name."""
        try:
            resolved = _resolve_gallery_item_from_name(item_name)
            if not resolved:
                return False

            route_key, index = resolved
            route = _get_gallery_route_by_key(route_key)

            if route:
                if unlock_route:
                    route.unlock_gallery()

                try:
                    route.unlock_item(index, False, True)
                except TypeError:
                    route.unlock_item(index, False)
            else:
                if unlock_route:
                    setattr(persistent, f"{route_key}_flag", True)
                setattr(persistent, f"gallery_{route_key}_{index}", True)

            renpy.save_persistent()
            return True
        except Exception as e:
            ap_debug(f"Error in ap_unlock_gallery_item_from_name({item_name}): {e}")
            return False

    def ap_handle_received_item(item_name: str, sender: str = "", net_item = None) -> None:
        """Handle AP item reception hooks and unlock gallery items when received from the server."""
        try:
            if ap_unlock_gallery_item_from_name(item_name, unlock_route=True):
                ap_info(f"Gallery item unlocked from server: {item_name}")
        except Exception as e:
            ap_debug(f"Error in ap_handle_received_item({item_name}): {e}")

    def ap_gallery_lock_images() -> bool:
        """
        Unlock every gallery route while keeping all gallery images locked.
        Useful when you want full gallery navigation without showing CGs.
        """
        try:
            route_groups = [
                globals().get("routesParent", []),
                globals().get("altRoutesParent", []),
                globals().get("routesParentLower", []),
            ]

            total_routes = 0
            total_images_locked = 0

            for group in route_groups:
                for route in group:
                    route.unlock_gallery()
                    total_routes += 1

                    for index in _get_gallery_item_numbers(route):
                        route.lock_item(index)
                        total_images_locked += 1

            renpy.save_persistent()
            ap_info(f"Gallery updated: {total_routes} routes unlocked, {total_images_locked} images locked.")
            return True
        except Exception as e:
            ap_debug(f"Error in ap_gallery_lock_images(): {e}")
            return False

    def ap_gallery_unlock_everything() -> bool:
        """
        Fully unlock every gallery route and every gallery image.
        """
        try:
            if "galleryInitializer" in globals() and galleryInitializer is not None:
                galleryInitializer.unlock_all_galleries_debug()
            else:
                # Fallback path if galleryInitializer is unavailable.
                route_groups = [
                    globals().get("routesParent", []),
                    globals().get("altRoutesParent", []),
                    globals().get("routesParentLower", []),
                ]

                for group in route_groups:
                    for route in group:
                        route.unlock_gallery()
                        for index in _get_gallery_item_numbers(route):
                            route.unlock_item(index, False)

            renpy.save_persistent()
            ap_info("Gallery updated: full unlock applied.")
            return True
        except Exception as e:
            ap_debug(f"Error in ap_gallery_unlock_everything(): {e}")
            return False



label chapter_requirements_failed:
    $ ap_info(f"{store.last_region_checked}: missing {store.last_region_failed_requirement}")
    ap "The time for this meeting has not yet come. Return when fate allows your paths to cross."
    menu:
        "Return to the main menu.":
            $ renpy.full_restart()
    return