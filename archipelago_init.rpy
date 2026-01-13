if True:
    define config.developer = True
    define config.autoreload = False
    define config.console = True
    define config.rollback_enabled = True

init -10 python:
    import os
    import sys
    
    # Configure paths for Archipelago client and dependencies
    candidates = []
    if "__file__" in globals():
        base_dir = os.path.dirname(__file__)
    else:
        base_dir = os.path.join(renpy.config.basedir, "game", "SlayThePrincessArchipelago")
    
    candidates.append(os.path.join(base_dir, "client"))
    candidates.append(os.path.join(base_dir, "client", "dependencies"))
    candidates.append(os.path.join(base_dir, "help"))
    candidates.append(base_dir)

    # Add all candidate paths to sys.path
    for candidate_path in candidates:
        if candidate_path and os.path.isdir(candidate_path) and candidate_path not in sys.path:
            sys.path.insert(0, candidate_path)

    def ap_notify(message):
        """Notification qui affiche ET écrit dans la console (Shift+O)"""
        msg_str = str(message)
        renpy.notify(msg_str)
        print(f"[AP] {msg_str}")
