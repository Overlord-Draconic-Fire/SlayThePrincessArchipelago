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
    $ config.allow_skipping = False
    ap "Another soul has fallen. Fate demands that you do the same."
    show screen black_overlay
    with dissolve
    $ other_skip_block_until = time.monotonic() + 5.0
    play voice3 "audio/voices/ch2/tower/_cont/princess/p40.flac"
    p "Everything goes dark, and you die."
    $ config.allow_skipping = True
    hide screen black_overlay
    $ renpy.full_restart()

image beast swallow screamer:
        "beast swallow anim1"
        0.0625
        "beast swallow anim2"
        0.0625
        "beast swallow anim3"
        0.0625
        "beast swallow anim4"
        0.0625
        "beast swallow anim5"
        0.0625
        "beast swallow anim6"
        0.0625
        "beast swallow anim7"
        0.0625
        "beast swallow anim8"
        0.0625
        "beast swallow anim9"
        0.0625
        "beast swallow anim10"
        0.0625
        "bg black"

label trap_hunted:
    play audio "audio/final/Beast_Roar_JUMPscare_1.flac"
    show beast swallow screamer onlayer front
    $ renpy.pause(0.7, hard=True, modal=False)
    hide beast onlayer front
    return

screen block_interaction():
    modal True
    zorder 1000

    key "dismiss" action NullAction()
    key "game_menu" action NullAction()
    key "rollback" action NullAction()

    button:
        xfill True
        yfill True
        background None
        action NullAction()

screen paranoid_text(message):
    zorder 100

    window:
        id "window"
        style "say_window"

        if paranoid.name is not None:
            window:
                id "namebox"
                style "namebox"

                text paranoid.name:
                    id "who"
                    style "say_label"
                    color "#ffffff"
                    outlines [(3, "#000000")]

        text (message + "{image=ctc_blink}"):
            id "what"
            style "voice_style"
            color "#ffffff"
            outlines [(3, "#000000")]

label trap_paranoid:
    $ config.allow_skipping = False
    show screen block_interaction

    play voice3 "audio/voices/ch2/nightmare/_encounter/paranoid/nm_loop_slow.flac"
    show screen paranoid_text("Heart... Lungs... Liver... Nerves...")
    show nightmare 2 1 onlayer front at Position(ypos=1125)
    $ renpy.pause(10.4, hard=True, modal=False)

    play voice3 "audio/voices/ch2/nightmare/_encounter/paranoid/nm_loop_1.flac"
    show screen paranoid_text("Heart. Lungs. Liver. Nerves.")
    show nightmare 2 2 onlayer front at Position(ypos=1125)
    $ renpy.pause(7.0, hard=True, modal=False)

    play voice3 "audio/voices/ch2/nightmare/_encounter/paranoid/nm_loop_mucho.flac"
    show screen paranoid_text("HEART. LUNGS. LIVER. NERVES.")
    show nightmare 2 3 onlayer front at Position(ypos=1125)
    $ renpy.pause(8.8, hard=True, modal=False)

    hide nightmare onlayer front
    hide screen block_interaction
    $ config.allow_skipping = True
    return

label trap_hero:
    $ config.allow_skipping = False
    $ other_skip_block_until = time.monotonic() + 5.0
    play music "audio/looping/party.ogg" loop
    show end good onlayer front at Position(ypos=1125)
    show text _("{color=000000}Good Ending! =:) YOU DID IT!!! you saved EVERYONE!{/color}") onlayer front at Position(ypos=950)
    play voice3 "audio/voices/ch2/prisoner/_basement/narrator/112.flac"
    n "That's great! Congratulations. You've earned it.\n"
    $ config.allow_skipping = True
    return

label trap_cheated:
    $ ap_notify(f"DeathLink: Received from Cheated", "ap")
    $ ap_debug("DeathLink applied")
    $ config.allow_skipping = False
    ap "Another soul has fallen. Fate demands that you do the same."
    show screen black_overlay
    with dissolve
    $ other_skip_block_until = time.monotonic() + 5.0
    play voice3 "audio/voices/ch2/tower/_cont/princess/p40.flac"
    p "Everything goes dark, and you die."
    $ other_skip_block_until = time.monotonic() + 2.0
    hide screen black_overlay
    play voice3 "audio/voices/ch3/razor/nexus/princess/28.flac"
    spmid "Gotcha!"
    $ config.allow_skipping = True
    return