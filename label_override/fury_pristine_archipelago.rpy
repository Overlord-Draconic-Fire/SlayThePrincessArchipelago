label fury_mirror_special_archipelago:
    python:
        send_heart_location(current_princess)

    if trait_cold:
        voice "audio/_pristine/voice/extras/cold/3.flac"
        cold "So that's a wrap. I didn't think we'd ever get here. There's only one thing left to do.\n"
    else:
        voice "audio/_pristine/voice/extras/broken/23.flac"
        broken "So the world's gone, and she's gone with it. There's only one thing left for you to do here. You need to look at yourself. Whatever you see, it's going to be okay.\n"

    menu:
        extend ""

        "{i}• [[Approach the mirror.]{/i}":
            hide mirror onlayer back
            show content m empty onlayer front at Position(ypos=1125)
            show mirror frame onlayer front at Position(ypos=1125)
            with Dissolve(2.0)
            truth "The voice falls silent as you approach.\n"
            menu:

                extend ""

                "{i}• [[Gaze into your reflection.]{/i}":
                    jump mirror_n_gaze_join

label fury_other_conclusion_archipelago:
    play tertiary "audio/final/fury_heart_loop.ogg" loop
    play sound "audio/_pristine/sfx/Apotheosis Oppresive AMB_2loop.flac" loop
    #play music "audio/_pristine/music/fury/The Fury Meta Intro.flac"
    #queue music "audio/_pristine/music/fury/The Fury Meta Loop.flac" loop
    # commenting out lines for hero + stubborn + broken below
    voice "audio/_pristine/voice/fury/narrator/63.flac"
    scene bg fury abs neutral onlayer back at Position(ypos=1125)
    show fury abs neutral onlayer front at Position(ypos=1125)
    with fade
    if persistent.quick_menu:
        $ quick_menu = True
    n "You are whole again, and in your body—the same body you arrived in. The Princess stands before you, her dress of skin more tattered than before, her face sullen.\n"
    if fury_source == "tower":
        voice "audio/_pristine/voice/fury/princess/46.flac"
        show fury abs neutral talk onlayer front
        with dissolve
        sp "It's all hollow. I ripped you to pieces. I broke your will. But it means nothing.\n"
        voice "audio/_pristine/voice/fury/princess/47.flac"
        show fury abs neutral talk upset onlayer front
        with Dissolve(1.0)
        sp "I am forever a piece unfinished. A song with no refrain.\n"
    else:
        #'of' extraneous, deleted
        voice "audio/_pristine/voice/fury/princess/48.flac"
        show fury abs neutral talk upset onlayer front
        with Dissolve(1.0)
        sp "After all that, why do I still feel so empty?\n"

    # All fake choices but the bottom

    $ config.menu_include_disabled = True
    menu:
        extend ""

        "{i}• ''Why did you keep me alive?''{/i}" if tower_false_choice:
            $ config.menu_include_disabled = False

        "{i}• ''I've been here so long.''{/i}" if tower_false_choice:
            $ config.menu_include_disabled = False

        "{i}• ''Everyone is gone.''{/i}" if tower_false_choice:
            $ config.menu_include_disabled = False

        "{i}• ''There's no one else here.''{/i}" if tower_false_choice:
            $ config.menu_include_disabled = False

        "{i}• ''I can't feel anything anymore.''{/i}" if tower_false_choice:
            $ config.menu_include_disabled = False

        "{i}• ''But still, I'm here. Watching.''{/i}" if tower_false_choice:
            $ config.menu_include_disabled = False

        "{i}• [[There is nothing for you to say.]{/i}":
            $ config.menu_include_disabled = False


    if fury_source == "tower":
        voice "audio/_pristine/voice/fury/princess/49.flac"
        show fury abs desperate talk onlayer front
        with Dissolve(1.0)
        $ gallery_fury.unlock_item(8)
        sp "We're so different. How could I ever hope for you to understand me?\n"
    else:
        voice "audio/_pristine/voice/fury/princess/50.flac"
        show fury abs desperate onlayer front
        with Dissolve(1.0)
        sp "If only you could see what I see. If only you could remember what I remember. If only you weren't so weak.\n"
        voice "audio/_pristine/voice/fury/princess/51.flac"
        show fury abs desperate talk onlayer front
        with dissolve
        sp "If only I could make you better. But... maybe I can.\n"
        $ gallery_fury.unlock_item(8)
        $ renpy.save_persistent()

    voice "audio/_pristine/voice/fury/narrator/64.flac"
    show fury abs begin onlayer front
    with Dissolve(1.0)
    n "She stands, arms outstretched, neck craned, gaze transfixed on something unseen above you both.\n"
    if fury_source == "tower":
        voice "audio/_pristine/voice/fury/princess/52.flac"
        sp "But perhaps there is a way to grant you understanding. Perhaps there is a way to make myself whole once more.\n"
    else:
        voice "audio/_pristine/voice/fury/princess/53.flac"
        sp "This will all be worth it. It has to be.\n"

    voice "audio/_pristine/voice/fury/narrator/65.flac"
    #play secondary "audio/final/Assorted_TapestyUnraveledBreakingRip_1.flac"
    play audio "audio/final/Spectre_HeartCrush_2 copy.flac"
    show player fury abs begin onlayer inyourface at Position(ypos=1125)
    with Dissolve(1.0)
    n "You are unwound again.\n"
    play audio "audio/_pristine/sfx/Fury Body Horror_19.flac"
    voice "audio/_pristine/voice/fury/narrator/66.flac"
    show bg fury abs sequence onlayer back
    show player fury abs sequence onlayer inyourface
    show fury abs sequence onlayer front
    with Dissolve(0.5)
    n "But it's different this time. Nothing slithers into your cells. You can feel something changing inside of you, but you see her changing, too.\n"
    play audio "audio/_pristine/sfx/Fury Body Horror_25.flac"
    voice "audio/_pristine/voice/fury/narrator/67.flac"
    hide player onlayer inyourface
    show bg fury abs sequence 2 onlayer back
    show fury abs sequence 2 onlayer front
    with Dissolve(1.0)
    n "Threads, strands of you, becoming pieces of something new. Something that's both you and her... oh no, absolutely not! You have to stop this, do you hear me? You have to stop this or the entire world ends—\n"
    play audio "audio/_pristine/sfx/Fury Body Horror_17.flac"
    show bg fury abs sequence 3 onlayer back
    show fury abs sequence 3 onlayer front
    with Dissolve(1.0)
    truth "But there is nothing left to stop anything. Your consciousness drifts towards hers.\n"
    if fury_source == "tower":
        voice "audio/_pristine/voice/fury/princess/54.flac"
        play audio "audio/_pristine/sfx/Fury Body Horror_1.flac"
        show bg fury abs sequence 4 onlayer back
        show fury abs sequence 4 onlayer front
        with Dissolve(1.0)
        sp "Yes. YES. See me as I have had to see you!\n"
        $ gallery_fury.unlock_item(9)
        $ renpy.save_persistent()
        play audio "audio/_pristine/sfx/Dragon Bubbling Flesh_3.flac"
        play secondary "audio/_music/mound/The Long Quiet Soft FINAL.ogg" loop fadein 15.0
        stop music fadeout 15.0
        stop sound fadeout 15.0
        stop tertiary fadeout 15.0
        hide fury onlayer front
        show bg fury abs sequence end onlayer back
        show quiet creep1 onlayer back at Position(ypos=1125)
        show rear fury abs sequence end onlayer front at Position(ypos=1125)
        show fury abs sequence end onlayer inyourface at Position(ypos=1125)
        with Dissolve(1.0)
        truth "You do. You see a towering heart, wounded and alone. One that is familiar to you, if distant.\n"
    else:
        play audio "audio/_pristine/sfx/Fury Body Horror_1.flac"
        voice "audio/_pristine/voice/fury/princess/55.flac"
        show bg fury abs sequence 4 onlayer back
        show fury abs sequence 4 onlayer front
        with Dissolve(1.0)
        sp "There doesn't have to be distance between us anymore. You feel it too, don't you?\n"
        play audio "audio/_pristine/sfx/Dragon Bubbling Flesh_3.flac"
        play secondary "audio/_music/mound/The Long Quiet Soft FINAL.ogg" loop fadein 15.0
        stop music fadeout 15.0
        stop sound fadeout 15.0
        stop tertiary fadeout 15.0
        hide fury onlayer front
        show bg fury abs sequence end onlayer back
        show quiet creep1 onlayer back at Position(ypos=1125)
        show rear fury abs sequence end onlayer front at Position(ypos=1125)
        show fury abs sequence end onlayer inyourface at Position(ypos=1125)
        with Dissolve(1.0)
        truth "You do. You feel as though you're coming home. A home you've forgotten, but one that never left your heart.\n"

    voice "audio/_pristine/voice/fury/princess/56.flac"
    show quiet creep3 onlayer back
    with Dissolve(1.0)
    sp "No... this isn't right. I feel... cold.\n"
    play audio "audio/final/assorted_Handsgrabbing_LIGHT_1.flac"
    hide fury onlayer inyourface
    hide rear onlayer front
    show hands fury abs 1 onlayer back at Position(ypos=1125)
    with Dissolve(1.0)
    $ renpy.pause(1.0)
    show hands fury abs 2 onlayer back at Position(ypos=1125)
    with Dissolve(1.0)
    $ renpy.pause(0.5)
    show hands fury abs 3 onlayer back at Position(ypos=1125)
    with Dissolve(0.5)
    $ renpy.pause(0.25)
    show hands fury abs 4 onlayer back at Position(ypos=1125)
    with Dissolve(0.25)
    $ renpy.pause(0.125)
    hide hands onlayer back
    with Dissolve(0.25)
    $ renpy.pause(0.125)
    $ blade_held = False
    $ default_mouse = "default"
    stop music
    hide bg onlayer back
    hide bg onlayer front
    hide player onlayer front
    hide player onlayer back
    hide fore onlayer front
    hide mid onlayer front
    hide fore onlayer inyourface
    hide farback onlayer farback
    hide bg onlayer back
    hide bg onlayer farback
    hide mid onlayer back
    hide stars onlayer farback
    hide bg onlayer back
    hide quiet onlayer back
    hide quiet onlayer farback
    hide quiet onlayer front
    show farback quiet onlayer farback at Position(ypos=1125)
    with Dissolve(4.0)
    show mirror quiet distant onlayer back at Position(ypos=1125)
    $ fury_end = "heart"
    $ princess_kept += 1
    $ princess_satisfy += 1
    $ current_princess = "furyheart"
    if loops_finished != 0:
        truth "The tethers that started to form between you have snapped. Your union has been halted. It's time for you to leave. Memory returns.\n"
    else:
        truth "The tethers that attempted to form between you have snapped. Your union has been halted. Something has taken her away, and it's left something else in her place.\n"
    
    python:
        send_heart_location(current_princess)
    
    menu:

        "{i}• [[Approach the mirror.]{/i}":
            hide mirror onlayer back
            show content m empty onlayer front at Position(ypos=1125)
            show mirror frame onlayer front at Position(ypos=1125)
            with Dissolve(2.0)
            truth "Silence as you approach.\n"
            menu:

                extend ""

                "{i}• [[Gaze into your reflection.]{/i}":
                    jump mirror_sort


    # END
