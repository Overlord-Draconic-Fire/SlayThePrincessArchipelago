init:

    $ renpy.music.register_channel(name = "secondary", mixer = "sfx", loop = False)
    $ renpy.music.register_channel(name = "tertiary", mixer = "sfx", loop = False)
    $ renpy.music.register_channel(name = "voice2", mixer = "voice", loop = False)

    $ renpy.music.register_channel(name = "music2", mixer = "music", loop = False)
    $ renpy.music.register_channel(name = "music3", mixer = "music", loop = False)
    $ renpy.music.register_channel(name = "music4", mixer = "music", loop = False)
    $ renpy.music.register_channel(name = "music5", mixer = "music", loop = False)

    $ renpy.music.register_channel(name = "musicgallery", mixer = "music", loop = True)

    default persistent.ctc = True
    default persistent.subtitles = True

    image ctc_opp_blink = ConditionSwitch("persistent.ctc == True", "ctc_opp_blink_on", "persistent.ctc == False", "gui/ctc_opp.png")

    image ctc_cold_blink = ConditionSwitch("persistent.ctc == True", "ctc_cold_blink_on", "persistent.ctc == False", "gui/ctc_cold.png")
    image ctc_hero_blink = ConditionSwitch("persistent.ctc == True", "ctc_hero_blink_on", "persistent.ctc == False", "gui/ctc_hero.png")


    image ctc_blink = ConditionSwitch("persistent.ctc == True", "ctc_blink_on", "persistent.ctc == False", "gui/empty_ctc.png")
    image ctc_blink_princess_default = ConditionSwitch("persistent.ctc == True", "ctc_blink_princess_default_on", "persistent.ctc == False", "gui/empty_ctc.png")
    image ctc_blink_princess_spooky = ConditionSwitch("persistent.ctc == True", "ctc_blink_princess_spooky_on", "persistent.ctc == False", "gui/empty_ctc.png")
    image ctc_truth_blink = ConditionSwitch("persistent.ctc == True", "ctc_truth_blink_on", "persistent.ctc == False", "gui/empty_ctc.png")

    image ctc_blink_on:
       "GUI/arrow.png"
       linear 0.75 alpha 1.0
       linear 0.75 alpha 0.0
       repeat

    image ctc_opp_blink_on:
        "GUI/ctc_opp.png"
        linear 0.75 alpha 1.0
        linear 0.75 alpha 0.0
        repeat

    image ctc_cold_blink_on:
        "GUI/ctc_cold.png"
        linear 0.75 alpha 1.0
        linear 0.75 alpha 0.0
        repeat

    image ctc_hero_blink_on:
        "GUI/ctc_hero.png"
        linear 0.75 alpha 1.0
        linear 0.75 alpha 0.0
        repeat

    image ctc_blink_princess_default_on:
        "gui/princess_ctc.png"
        linear 0.75 alpha 1.0
        linear 0.75 alpha 0.0
        repeat

    image ctc_blink_princess_spooky_on:
        "gui/spooky_ctc.png"
        linear 0.75 alpha 1.0
        linear 0.75 alpha 0.0
        repeat

    image ctc_truth_blink_on:
        "gui/truth_ctc.png"
        linear 0.75 alpha 1.0
        linear 0.75 alpha 0.0
        repeat

    define y = Character("You", color = "#ffffff")
    define sp = Character(_("The Princess"), color = "#ffffff00", what_color = "#e44646", what_outlines=[ (2, "#4f1313") ], what_style = "window_spooky_princess", ctc="ctc_blink_princess_spooky", ctc_position="nestled")

    define spright = Character(_("The Princess"), color = "#ffffff00", what_color = "#e44646", what_outlines=[ (2, "#4f1313") ], what_style = "window_spooky_princess_right", ctc="ctc_blink_princess_spooky", ctc_position="nestled")

    define spmid = Character(_("The Princess"), color = "#ffffff00", what_color = "#e44646", what_outlines=[ (2, "#4f1313") ], what_style = "window_spooky_princess_mid", ctc="ctc_blink_princess_spooky", ctc_position="nestled")

    define p = Character(_("The Princess"), color = "#ffffff00", what_color = "#fadbe4", what_outlines=[ (2, "#622929") ], what_style = "window_princess", ctc="ctc_blink_princess_default", ctc_position="nestled")

    define stranger = Character(_("The Princess"), color = "#ffffff00", what_color = "#fadbe4", what_outlines=[ (2, "#622929") ], what_style = "window_princess", ctc="ctc_blink_princess_default", ctc_position="nestled")

    define pmid = Character(_("The Princess"), color = "#ffffff00", what_color = "#fadbe4", what_outlines=[ (2, "#622929") ], what_style = "window_princess_mid", ctc="ctc_blink_princess_default", ctc_position="nestled")
    #define p = Character("", color = "#ffffff", what_color = "#BA7DB8", what_outlines=[ (1, "#FF00FF") ], what_style = "window_princess", what_font = "gui/fonts/AmaticSC-bold.ttf", what_size = 60)
    #define n = Character("The Narrator", color = "#ffffff", what_color = "#ffffff")

    define wp = Character(_("The Princess"), what_color = "#fadbe4", color = "#fadbe4", what_text_align=0.5, what_outlines=[ (2, "#622929") ], who_outlines= [ (2, "#622929") ], what_style = "wild_style", who_style = "wild_style_who", ctc="ctc_blink_princess_default", ctc_position="nestled")

    define swp = Character(_("The Princess"), color = "#e44646", what_style = "spooky_wild_style", who_style = "spooky_wild_style_who", what_color = "#e44646", what_outlines=[ (2, "#4f1313") ], who_outlines= [ (2, "#622929") ], ctc="ctc_blink_princess_spooky", ctc_position="nestled")

    define n = Character(_("The Narrator"), color = "#ffffff", what_color = "#ffffff", what_text_align=0.5, what_outlines=[ (3, "#000000") ], who_outlines= [ (3, "#000000") ], what_style = "voice_style", ctc="ctc_blink", ctc_position="nestled")

    define np = Character(_("The Narrator"), color = "#fadbe4", what_color = "#fadbe4", what_outlines=[ (2, "#622929") ], what_text_align=0.5, who_outlines= [ (3, "#622929") ], what_style = "voice_style", ctc="ctc_blink", ctc_position="nestled")

    define mirror = Character(_("The Narrator"), color = "#ffffff", what_color = "#ffffff", what_text_align=0.5, what_outlines=[ (3, "#000000") ], who_outlines= [ (3, "#000000") ], what_style = "voice_style", ctc="ctc_blink", ctc_position="nestled")

    define hero = Character(_("Voice of the Hero"), color = "#ffffff", what_text_align=0.5, what_outlines=[ (3, "#000000") ], who_outlines= [ (3, "#000000") ], what_style = "voice_style", ctc="ctc_blink", ctc_position="nestled")

    define previous_dialogue = ""
    define speaker = ""
    define player_name = ""
    default trait_hero = False
    default current_princess = ""
    default loop_1_princess_killed = False


    # defining objective speaker
    define truth = Character("", color = "#ffffff", what_outlines=[ (3, "#000000") ], who_outlines= [ (3, "#000000") ], what_style = "truth_style", ctc="ctc_truth_blink", ctc_position="nestled", what_slow_cps = 45)

    define truthsmall = Character("", color = "#ffffff", what_outlines=[ (3, "#000000") ], who_outlines= [ (3, "#000000") ], what_style = "truth_small_style", ctc="ctc_truth_blink", ctc_position="nestled", what_slow_cps = 45)


    define truthmid = Character("", color = "#ffffff", what_outlines=[ (3, "#000000") ], who_outlines= [ (3, "#000000") ], what_style = "truth_mid_style", ctc="ctc_truth_blink", ctc_position="nestled", what_slow_cps = 45)

    define truthside = Character("", color = "#ffffff", what_outlines=[ (3, "#000000") ], who_outlines= [ (3, "#000000") ], what_style = "truth_side_style", ctc="ctc_truth_blink", ctc_position="nestled", what_slow_cps = 45)

    # stranger
    default trait_contrarian = False
    define contrarian = Character(_("Voice of the Contrarian"), color = "#ffffff", what_outlines=[ (3, "#000000") ], who_outlines= [ (3, "#000000") ], what_style = "voice_style", ctc="ctc_blink", ctc_position="nestled")

    # Spectre
    default trait_cold = False
    define cold = Character(_("Voice of the Cold"), color = "#ffffff", what_outlines=[ (3, "#000000") ], who_outlines= [ (3, "#000000") ], what_style = "voice_style", ctc="ctc_blink", ctc_position="nestled")

    # Tower
    default trait_broken = False
    define broken = Character(_("Voice of the Broken"), color = "#ffffff", what_outlines=[ (3, "#000000") ], who_outlines= [ (3, "#000000") ], what_style = "voice_style", ctc="ctc_blink", ctc_position="nestled")

    # Beast
    default trait_hunted = False
    define hunted = Character(_("Voice of the Hunted"), color = "#ffffff", what_outlines=[ (3, "#000000") ], who_outlines= [ (3, "#000000") ], what_style = "voice_style", ctc="ctc_blink", ctc_position="nestled")

    # prisoner
    default trait_skeptic = False
    define skeptic = Character(_("Voice of the Skeptic"), color = "#ffffff", what_outlines=[ (3, "#000000") ], who_outlines= [ (3, "#000000") ], what_style = "voice_style", ctc="ctc_blink", ctc_position="nestled")

    # adversary
    default trait_stubborn = False
    define stubborn = Character(_("Voice of the Stubborn"), color = "#ffffff", what_outlines=[ (3, "#000000") ], who_outlines= [ (3, "#000000") ], what_style = "voice_style", ctc="ctc_blink", ctc_position="nestled")

    # damsel
    default trait_smitten = False
    define smitten = Character(_("Voice of the Smitten"), color = "#ffffff", what_outlines=[ (3, "#000000") ], who_outlines= [ (3, "#000000") ], what_style = "voice_style", ctc="ctc_blink", ctc_position="nestled")

    # razor
    default trait_flinching = False
    define flinching = Character(_("Voice of the Flinching"), color = "#ffffff", what_outlines=[ (3, "#000000") ], who_outlines= [ (3, "#000000") ], what_style = "voice_style", ctc="ctc_blink", ctc_position="nestled")

    #nightmare
    default trait_paranoid = False
    define paranoid = Character(_("Voice of the Paranoid"), color = "#ffffff", what_outlines=[ (3, "#000000") ], who_outlines= [ (3, "#000000") ], what_style = "voice_style", ctc="ctc_blink", ctc_position="nestled")

    #witch
    default trait_opportunist = False
    define opportunist = Character(_("Voice of the Opportunist"), color = "#ffffff", what_outlines=[ (3, "#000000") ], who_outlines= [ (3, "#000000") ], what_style = "voice_style", ctc="ctc_blink", ctc_position="nestled")

    # razor-alt
    default trait_cheated = False
    define cheated = Character(_("Voice of the Cheated"), color = "#ffffff", what_outlines=[ (3, "#000000") ], who_outlines= [ (3, "#000000") ], what_style = "voice_style", ctc="ctc_blink", ctc_position="nestled")


    # double talk
    define stubcont = Character(_("Voices of the Stubborn and Contrarian"), color = "#ffffff", what_outlines=[ (3, "#000000") ], who_outlines= [ (3, "#000000") ], what_style = "voice_style", ctc="ctc_blink", ctc_position="nestled")

    define parskep = Character(_("Voices of the Paranoid and Skeptic"), color = "#ffffff", what_outlines=[ (3, "#000000") ], who_outlines= [ (3, "#000000") ], what_style = "voice_style", ctc="ctc_blink", ctc_position="nestled")


    # princess and the dragon guys

    define opportunistdragon = Character("???", color = "#ffffff00", what_color = "#A77341", what_outlines=[ (2, "#4f1313") ], what_style = "opportunist_dragon_style", ctc="ctc_opp_blink", ctc_position="nestled")

    define herodragon = Character("???", color = "#ffffff00", what_color = "D7ECF5", what_outlines=[ (3, "#00557A") ], what_style = "hero_dragon_style", ctc="ctc_hero_blink", ctc_position="nestled")

    define colddragon = Character("???", color = "#ffffff00", what_color = "#BDC5DA", what_outlines=[ (3, "#000000") ], what_style = "cold_dragon_style", ctc="ctc_cold_blink", ctc_position="nestled")


    # Archipelago characters

    define onilaf = Character("Onilaf", color = "#ffffff", what_color = "#ffffff", what_text_align=0.5, what_outlines=[ (3, "#000000") ], who_outlines= [ (3, "#000000") ], what_style = "voice_style", ctc="ctc_blink", ctc_position="nestled")