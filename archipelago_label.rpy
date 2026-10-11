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
    ap "Another soul has fallen. Fate demands that you do the same."
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

label trap_paranoid:
    $ config.allow_skipping = False
    show screen block_interaction

    play voice3 "audio/voices/ch2/nightmare/_encounter/paranoid/nm_loop_slow.flac"
    show nightmare 2 1 onlayer front at Position(ypos=1125)
    $ renpy.pause(10.4, hard=True, modal=False)

    play voice3 "audio/voices/ch2/nightmare/_encounter/paranoid/nm_loop_1.flac"
    show nightmare 2 2 onlayer front at Position(ypos=1125)
    $ renpy.pause(7.0, hard=True, modal=False)

    play voice3 "audio/voices/ch2/nightmare/_encounter/paranoid/nm_loop_mucho.flac"
    show nightmare 2 3 onlayer front at Position(ypos=1125)
    $ renpy.pause(8.8, hard=True, modal=False)

    hide nightmare onlayer front
    hide screen block_interaction
    $ config.allow_skipping = True
    return

init python:
    import time

    _say_minimum_until = 0.0

    def allow_say_dismiss():
        return time.time() >= _say_minimum_until

    config.say_allow_dismiss = allow_say_dismiss

label trap_hero:
    $ config.allow_skipping = False
    play music "audio/looping/party.ogg" loop
    show end good onlayer front at Position(ypos=1125)
    show text _("{color=000000}Good Ending! =:) YOU DID IT!!! you saved EVERYONE!{/color}") onlayer front at Position(ypos=950)
    play voice3 "audio/voices/ch2/prisoner/_basement/narrator/112.flac"
    $ _say_minimum_until = time.time() + 5.0
    n "That's great! Congratulations. You've earned it.\n"
    $ config.allow_skipping = True
    return