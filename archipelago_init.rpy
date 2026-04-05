if True:
    define config.developer = True
    define config.autoreload = False
    define config.console = True
    define config.rollback_enabled = True

init -10 python:
    import os
    import sys
    
    # Force le bon chemin absolu
    base_dir = os.path.join(renpy.config.basedir, "game")
    
    # Chemins à ajouter dans l'ordre de priorité
    paths_to_add = [
        os.path.join(base_dir, "client", "dependencies"),
        os.path.join(base_dir, "client"),
        os.path.join(base_dir, "help"),
        base_dir
    ]
    
    # Ajoute TOUS les chemins
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
            """Accès thread-safe à archipelago_client depuis n'importe quel thread"""
            with self.lock:
                return self.client
        
        def set_client(self, client):
            """Modification thread-safe de archipelago_client"""
            with self.lock:
                self.client = client
    
    # Global instance
    archipelago = ArchipelagoManager()

    def ap_notify(message) -> None:
        """Notification qui affiche ET écrit dans la console (Shift+O)"""
        msg_str = str(message)
        renpy.notify(msg_str)
        print(f"[AP] {msg_str}")

    def get_archipelago_client() -> RenpyContext:
        """Accès thread-safe à archipelago_client depuis n'importe quel thread"""
        return archipelago.get_client()
    
    def set_archipelago_client(client: RenpyContext) -> None:
        """Modification thread-safe de archipelago_client"""
        archipelago.set_client(client)

    def send_location(location_name : str) -> None:
        """Envoie une location arbitraire."""
        try:
            client : RenpyContext = get_archipelago_client()
            if client:
                client.send_location(location_name)
            else:
                ap_notify(f"archipelago_client non initialisé")
        except Exception as e:
            import traceback
            ap_notify(f"Erreur lors de l'envoi de location: {e}")
            traceback.print_exc()
    
    def hasThisDagger(dagger_value : str) -> bool:
        """
        Vérifie si le joueur possède un dagger.
        Accepte une valeur d'item comme Item.dagger_wild et retourne True si :
        - Le joueur a la dagger spécifique, OU
        - Le joueur a la dagger du chapitre (dagger3 pour chapter 3), OU
        - Le joueur a la dagger global (dagger)
        """
        try:
            client : RenpyContext = get_archipelago_client()
            if not client:
                ap_notify(f"archipelago_client non initialisé")
                return False

            # Vérifier la dagger spécifique
            if client.has_item(dagger_value):
                ap_notify(f"Player has specific dagger: {dagger_value}")
                return True
            
            # Vérifier la dagger du chapitre correspondant
            if dagger_value in DAGGER_CHAPTER_MAP.DAGGER_CHAPTER_MAP:
                chapter = DAGGER_CHAPTER_MAP.DAGGER_CHAPTER_MAP[dagger_value]
                if chapter != "special":
                    chapter_dagger = f"dagger{chapter}"
                    chapter_item = getattr(Item, chapter_dagger)
                    if client.has_item(chapter_item):
                        ap_notify(f"Player has chapter dagger: {chapter_item}")
                        return True
            
            # Vérifier la dagger global
            if client.has_item(Item.dagger):
                ap_notify(f"Player has global dagger: {Item.dagger}")
                return True
            
            return False
        except Exception as e:
            ap_notify(f"Error in hasThisDagger({dagger_value}): {e}")
            return False

    def hasRegionRequirements(region_value : str) -> bool:
        """
        Vérifie si le joueur possède tous les items requis pour une région.
        Le paramètre doit être une valeur de région (ex: Region.needle_hunted).
        """
        try:
            client = get_archipelago_client()
            if not client:
                return False

            requirements = REGION_REQUIREMENTS.REGION_REQUIREMENTS.get(region_value)
            if not requirements:
                ap_notify(f"No requirements found for region: {region_value}")
                return False

            for required_item in requirements:
                if not client.has_item(required_item):
                    return False

            return True
        except Exception as e:
            ap_notify(f"Error in hasRegionRequirements({region_value}): {e}")
            return False



label chapter_requirements_failed:
    $ ap_notify(f"{current_princess}: missing region requirements")
    ap "The time for this meeting has not yet come. Return when fate allows your paths to cross."
    menu:
        "Return to the main menu.":
            $ renpy.full_restart()
    return