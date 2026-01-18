if True:
    define config.developer = True
    define config.autoreload = False
    define config.console = True
    define config.rollback_enabled = True

init -10 python:
    import os
    import sys
    
    # Force le bon chemin absolu
    base_dir = os.path.join(renpy.config.basedir, "game", "SlayThePrincessArchipelago")
    
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
    import RenpyClient
    import Utils
    import threading
    import asyncio
    import websockets
    
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
                print(f"[AP] Client set to: {client}")
    
    # Global instance
    archipelago = ArchipelagoManager()
    
    def ap_notify(message):
        """Notification qui affiche ET écrit dans la console (Shift+O)"""
        msg_str = str(message)
        renpy.notify(msg_str)
        print(f"[AP] {msg_str}")

    def get_archipelago_client():
        """Accès thread-safe à archipelago_client depuis n'importe quel thread"""
        return archipelago.get_client()
    
    def set_archipelago_client(client):
        """Modification thread-safe de archipelago_client"""
        archipelago.set_client(client)

    def send_heart_location(current_princess):
        try:
            from CURRENT_PRINCESS_TO_HEART_LOCATION import CURRENT_PRINCESS_TO_HEART_LOCATION
            
            client = get_archipelago_client()
            if client and current_princess in CURRENT_PRINCESS_TO_HEART_LOCATION:
                location_name = CURRENT_PRINCESS_TO_HEART_LOCATION[current_princess]
                client.send_location(location_name)
            elif client:
                ap_notify(f"current_princess '{current_princess}' non mappé dans CURRENT_PRINCESS_TO_HEART_LOCATION")
            else:
                ap_notify(f"archipelago_client non initialisé")
        except Exception as e:
            import traceback
            ap_notify(f"Erreur lors de l'envoi de location: {e}")
            traceback.print_exc()
