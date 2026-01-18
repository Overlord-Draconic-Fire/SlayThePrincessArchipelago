label start_2_archipelago:
    python:
        send_princess_location(current_princess)

    stop music
    stop sound
    stop secondary
    $ default_mouse = "default"
    $ blade_held = False
    $ current_loop = 2
    $ quick_menu = False
    $ config.menu_include_disabled = False

    if current_princess == "adversary":
        $ adversary_encountered = True
        jump adversary_1_start

    elif current_princess == "beast":
        $ beast_encountered = True
        jump beast_1_start

    elif current_princess == "damsel":
        $ damsel_encountered = True
        jump damsel_1_start

    elif current_princess == "nightmare":
        $ nightmare_encountered = True
        jump nightmare_1_start

    elif current_princess == "prisoner":
        $ prisoner_encountered = True
        jump prisoner_1_start

    elif current_princess == "razor":
        $ razor_encountered = True
        jump razor_1_start

    elif current_princess == "spectre":
        $ spectre_encountered = True
        jump spectre_1_start

    elif current_princess == "stranger":
        $ stranger_encountered = True
        jump stranger_1_start

    elif current_princess == "tower":
        $ tower_encountered = True
        jump tower_1_start

    elif current_princess == "witch":
        $ witch_encountered = True
        jump witch_1_start

    else:
        $ stranger_encountered = True
        jump stranger_1_start

return
