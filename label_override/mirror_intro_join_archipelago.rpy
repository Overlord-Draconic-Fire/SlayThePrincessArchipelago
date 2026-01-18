# Archipelago Override: Mirror Labels
# These labels are overridden from game/scripts/special/mirror/mirror_intro_join.rpy
# They allow us to hook into Archipelago logic without modifying the original game files.

label mirror_nightmare_2_archipelago:
    python:
        send_heart_location(current_princess)

    $ nightmare_2_finished = True
    menu:
        extend ""

        "{i}• [[Approach the mirror.]{/i}":
            hide mirror onlayer back
            show content m empty onlayer front at Position(ypos=1125)
            show mirror frame onlayer front at Position(ypos=1125)
            with Dissolve(2.0)
            jump mirror_nightmare_2_wipe

label mirror_start_2_archipelago:
    python:
        send_heart_location(current_princess)

    if current_run_mirror_comment or current_run_mirror_touched:
        voice "audio/voices/mirror/intro/hero/3.flac"
        hero "And there's that mirror again. Why is it here? Why now?!\n"
    else:
        voice "audio/voices/mirror/intro/hero/4.flac"
        hero "And is that a... mirror? Why is it here? Why now?!\n"

    $ mirror_comfort_count = 0
    if loops_finished == 0:
        $ mirror_1_where_princess = False
        $ mirror_1_narrator_gone = False
        $ mirror_1_mirror_suggest = False
        $ mirror_hero_scared_flag = True
        jump mirror_1_menu
    else:
        jump mirror_n_menu

label mirror_sort_archipelago:
    python:
        send_heart_location(current_princess)

    hide chain onlayer front
    hide chain onlayer back

    if loops_finished == 0:
        jump mirror_1_join

    elif loops_finished == 1:
        jump mirror_2_join

    elif loops_finished == 2:
        jump mirror_3_join

    elif loops_finished == 3:
        jump mirror_4_join

    else:
        jump mirror_finale


return
