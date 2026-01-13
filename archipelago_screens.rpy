default server_url = "wss://archipelago.gg:51489"
default slot_name = "Onilaf"
default password = ""

screen main_menu():
    ## This ensures that any other menu screen is replaced.
    tag menu
    modal True

    if persistent.performance_mode == False and persistent.flickering:
        add Movie(size=(1920, 1080), channel="mm_movie")
        on "show" action Play("mm_movie", "images/menu/main_menu.webm", loop=True)
        on "hide" action Stop("mm_movie")
        on "hide" action Hide(screen = "navigation")
        on "replace" action Play("mm_movie", "images/menu/main_menu.webm", loop=True)
        on "replace" action Show(screen = "navigation")
        on "replaced" action Stop("mm_movie")
    else:
        add "menu static"
    #add "choices_backdrop_menu"
    #add "logo_menu_final"
    add "logo_menu_pristine"

    vbox:
        style_prefix "main_menu"
        xalign 0.5
        #xpos 1737
        xpos 237
        yanchor 0
        yoffset 230

        spacing gui.navigation_spacing


    # add this where appropriate
        if renpy.newest_slot != None:

            textbutton _("Continue") action Continue() default_focus True
    
        textbutton _("New Game") action Start() default_focus True

        textbutton _("Load Game") action ShowMenu("load") default_focus True

        textbutton _("Preferences") action ShowMenu("preferences")

        if renpy.variant("pc") or (renpy.variant("web") and not renpy.variant("mobile")):
            ## Help isn't necessary or relevant to mobile devices.
            textbutton _("Controls") action ShowMenu("help")

        if not renpy.variant("console"):
            textbutton _("Accessibility") action ToggleScreen("_accessibility")

        if persistent.gallery_unlocked:
            textbutton _("Memories") action [ShowMenu("gallery"), Play("musicgallery", "audio/_music/mound/Oblivion.flac"), PauseAudio("music", True), PauseAudio("music2", True),PauseAudio("music3", True),PauseAudio("music4", True),PauseAudio("music5", True),PauseAudio("sound", True),PauseAudio("secondary", True),PauseAudio("tertiary", True)]

        if persistent.gallery_unlocked:
            textbutton _("Reset Gallery") action [Confirm(_("Are you sure you want to clear your gallery progress? This action cannot be undone."), yes = Function(galleryInitializer.reset_galleries))]

        textbutton _("Subtitle Language") action ShowMenu("language_select_menu")

        if renpy.variant("pc"):
            textbutton _("Join Our Discord") action OpenURL("https://discord.gg/blacktabbygames")

        if renpy.variant("pc"):
            ## The quit button is banned on iOS and unnecessary on Android and
            ## Web.
            textbutton _("Quit") action Quit(confirm=not main_menu)

    if gui.show_name:
        vbox:
            style "main_menu_vbox"

            text "[config.name!t]":
                style "main_menu_title"

            text "[config.version]":
                style "main_menu_version"

    frame:
        xalign 1.0
        yalign 0.0
        xsize 700
        xmargin 20
        ymargin 20
        background "#0008"
        padding (20, 20)

        vbox:
            spacing 15

            # Titre
            label _("Connexion à Archipelago")
            
            textbutton "Connexion" action Function(websocket_thread)

init python:
    import threading
    import asyncio
    import websockets
    import RenpyClient
    import Utils

    # Pre-fill fields from previous session if available.
    try:
        persistent_client_data = Utils.persistent_load().get("client", {})
        if persistent_client_data.get("last_server_address"):
            last_addr = persistent_client_data["last_server_address"]
            if last_addr.startswith("ws://") or last_addr.startswith("wss://"):
                server_url = last_addr
            else:
                server_url = f"wss://{last_addr}"
        if persistent_client_data.get("last_slot_name"):
            slot_name = persistent_client_data["last_slot_name"]
    except Exception:
        pass

    global archipelago_client

    def websocket_thread():
        new_connect_websocket(server_url, slot_name, password)

    def new_connect_websocket(url, name, mdp):
        def run_connection():
            global archipelago_client
            async def connect_and_listen():
                global archipelago_client
                ap_notify("Démarrage connexion...")
                archipelago_client = RenpyClient.create_renpy_client(
                    url, name, mdp,
                    on_text=ap_notify,
                )
                ap_notify("Client créé, connexion en cours...")
                await archipelago_client.connect(url)
                ap_notify("Connecté avec succès !")
                # Keep connection alive by listening for messages
                ap_notify("Démarrage message loop...")
                await archipelago_client.message_loop()
                await archipelago_client.shutdown()
            
            try:
                asyncio.run(connect_and_listen())
            except Exception as e:
                import traceback
                error_msg = f"Erreur de connexion: {str(e)}"
                ap_notify(error_msg)
                traceback.print_exc()
        
        ap_notify("Lancement du thread...")
        t = threading.Thread(target=run_connection)
        t.daemon = True
        t.start()
        ap_notify("Thread lancé !")