label razor_final_mirror_archipelago:
    python:
        send_heart_location(current_princess)

    menu:
        extend ""

        "{i}• [[Approach the mirror.]{/i}":
            hide mirror onlayer back
            show content m empty onlayer front at Position(ypos=1125)
            show mirror frame onlayer front at Position(ypos=1125)
            with Dissolve(2.0)
            truth "You do so.\n"
            jump mirror_n_wipe
return