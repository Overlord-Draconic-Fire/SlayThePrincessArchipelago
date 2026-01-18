label contrarian_pristine_apoth_menu_archipelago:
    $ contrarian_pristine_apoth_menu_explore = False
    menu:
        extend ""

        "{i}• (Explore) Hey, funny one, didn't you say something about a third option earlier? One that would make everyone unhappy?{/i}" if contrarian_pristine_apoth_menu_explore == False:
            $ contrarian_pristine_apoth_menu_explore = True
            if apotheosis_run:
                voice "audio/_pristine/voice/apotheosis/contrarian/10.flac"
                contrarian "I dunno! I'm at loss. What if we... run away again? I'm sure it'll work this time.\n"
            else:
                voice "audio/_pristine/voice/apotheosis/contrarian/11a.flac"
                contrarian "Well, we could always run away, right?\n"
            voice "audio/_pristine/voice/apotheosis/hero/7.flac"
            hero "To where?\n"
            if apotheosis_run:
                voice "audio/_pristine/voice/apotheosis/contrarian/12.flac"
                contrarian "Anywhere!\n"
            else:
                voice "audio/_pristine/voice/apotheosis/contrarian/13.flac"
                contrarian "I dunno. Anywhere!\n"
            voice "audio/_pristine/voice/apotheosis/broken/4.flac"
            broken "You're all ruining the moment of her ascension. Have you no respect for the divine?\n"
            jump contrarian_pristine_apoth_menu

        "{i}• [[Take the blade.]{/i}":
            voice "audio/_pristine/voice/apotheosis/narrator/5.flac"
            $ blade_held = True
            $ default_mouse = "thumb"
            play audio "audio/one_shot/knife_pickup.flac"
            hide blade onlayer front
            show player apotheosis blade tree onlayer inyourface at Position(ypos=1125)
            with dissolve
            n "With a grim determination, you yank the blade from the trunk.\n"
            voice "audio/_pristine/voice/apotheosis/contrarian/14.flac"
            hide player onlayer inyourface
            hide fore onlayer front
            hide mid onlayer back
            hide stars onlayer farback
            show stars apotheosis charge onlayer farback at Position(ypos=1125)
            show apotheosis charge onlayer back at Position(ypos=1125)
            show fore apotheosis charge onlayer front at Position(ypos=1125)
            show player apotheosis charge onlayer inyourface at Position(ypos=1125)
            with Dissolve(1.0)
            contrarian "Yeah. This feels right. She doesn't get to just smugly stand over us like we don't matter. Let's take her down a peg.\n"
            voice "audio/_pristine/voice/apotheosis/broken/5.flac"
            broken "You're not going to win. You know that, right? What are you going to do with that tiny blade? Give her a scratch?\n"
            voice "audio/_pristine/voice/apotheosis/hero/8.flac"
            hero "Even if that's all we manage, I'd rather go down swinging.\n"
            voice "audio/_pristine/voice/apotheosis/contrarian/15.flac"
            contrarian "See how everything's floating around her? I bet we could make it if we just jumped really hard.\n"
            voice "audio/_pristine/voice/apotheosis/narrator/6.flac"
            hide stars onlayer farback
            hide apotheosis onlayer back
            hide fore onlayer front
            hide player onlayer inyourface
            with fade
            scene bg black
            with fade
            n "You gather yourself, closing your eyes and shutting out the towering vision of the Princess. There is only her, and you. That's all there ever was.\n"
            voice "audio/_pristine/voice/apotheosis/narrator/7.flac"
            show stars apotheosis charge onlayer farback at Position(ypos=1125)
            show apotheosis charge onlayer back at Position(ypos=1125)
            show fore apotheosis charge onlayer front at Position(ypos=1125)
            show player apotheosis charge onlayer inyourface at Position(ypos=1125)
            with fade
            n "It's time to face her.\n"
            menu:
                extend ""

                "{i}• [[Charge into oblivion.]{/i}":
                    $ quick_menu = False
                    voice "audio/_pristine/voice/apotheosis/narrator/8.flac"
                    play tertiary "audio/one_shot/footstep_run_dirt_short.flac"
                    queue tertiary "audio/final/den_emerge.flac"
                    hide stars onlayer farback
                    hide apotheosis onlayer back
                    hide fore onlayer front
                    hide player onlayer inyourface
                    with fade
                    show stars apotheosis charge 2 onlayer farback at Position(ypos=1125)
                    show bg apotheosis charge 2 onlayer back at Position(ypos=1125)
                    show apotheosis charge 2 onlayer back at Position(ypos=1125)
                    show fore apotheosis charge 2 onlayer front at Position(ypos=1125)
                    show player apotheosis charge onlayer inyourface at Position(ypos=1125)
                    with fade
                    if persistent.quick_menu:
                        $ quick_menu = True
                    n "You launch yourself towards the Princess. The pull of her gravity catches you, carrying you across the ground into the violent swirl of her orbit.\n"
                    $ gallery_apotheosis.unlock_item(3)
                    $ renpy.save_persistent()
                    voice "audio/_pristine/voice/apotheosis/princess/1.flac"
                    play audio "audio/final/Tower_WindWHistlingFly_oneshot_1.flac"
                    hide stars onlayer farback
                    hide apotheosis onlayer back
                    hide fore onlayer front
                    show stars apotheosis charge 3 onlayer farback at Position(ypos=1125)
                    show bg apotheosis charge 3 onlayer back at Position(ypos=1125)
                    show apotheosis charge 3 onlayer back at Position(ypos=1125)
                    show fore apotheosis charge 3 onlayer front at Position(ypos=1125)
                    with Dissolve(2.0)
                    sp "Such defiance, even now. Do it, then. Show me what you think it takes to end that which is destined to end everything.\n"
                    voice "audio/_pristine/voice/apotheosis/broken/6.flac"
                    show apotheosis charge 3 onlayer back at Position(ypos=1125)
                    with dissolve
                    broken "Don't you see how hopeless this is? She fears nothing.\n"
                    voice "audio/_pristine/voice/apotheosis/contrarian/16a.flac"
                    contrarian "That's right, she doesn't. So she has no idea what she's in for.\n"

            voice "audio/_pristine/voice/apotheosis/narrator/9.flac"
            play audio "audio/final/Adversary_BPlayerAggressivelyThrown_1.flac"
            hide stars onlayer farback
            hide bg onlayer back
            hide apotheosis onlayer back
            hide player onlayer inyourface
            hide fore onlayer front
            show farback apotheosis chest onlayer farback at Position(ypos=1125)
            show apotheosis chest onlayer front at Position(ypos=1125)
            show debris apotheosis chest onlayer inyourface at Position(ypos=1125)
            with Dissolve(1.0)
            n "With a heavy thump, you land on her chest.\n"
            voice "audio/_pristine/voice/apotheosis/hero/9.flac"
            hero "It's now or never. We've come this far, let's take it home.\n"
            menu:
                extend ""

                "{i}• [[Carve into her divine heart.]{/i}":
                    $ gallery_apotheosis.unlock_item(9)
                    $ renpy.save_persistent()
                    voice "audio/_pristine/voice/apotheosis/narrator/10.flac"
                    play audio "audio/_pristine/sfx/apotheosis_knife_doomed.flac"
                    show apotheosis chest slash 1 onlayer front
                    with dissolve
                    n "You strike, but her skin is like steel. Though you stab at her again and again, the wounds are superficial, mere etchings in a sprawling surface.\n"
                    voice "audio/_pristine/voice/apotheosis/broken/7.flac"
                    show apotheosis chest slash 2 onlayer front
                    with dissolve
                    broken "You see? It was always pointless. All this has done is bring us close to her... and how beautiful it is, to be so close.\n"
                    voice "audio/_pristine/voice/apotheosis/hero/10.flac"
                    hero "It's not pointless, it can't be! We wouldn't be here if there wasn't some hope we could succeed.\n"

            voice "audio/_pristine/voice/apotheosis/princess/2.flac"
            show apotheosis chest onlayer front
            with Dissolve(1.0)
            sp "Is that all?\n"
            $ quick_menu = False
            voice "audio/_pristine/voice/apotheosis/narrator/11.flac"
            play secondary "audio/final/den_emerge.flac"
            queue secondary "audio/one_shot/door_stone.flac"
            hide farback onlayer farback
            hide debris onlayer inyourface
            hide apotheosis onlayer front
            hide player onlayer inyourface
            scene bg black
            with fade
            show farback apotheosis pluck onlayer farback at Position(ypos=1125)
            show debris apotheosis pluck onlayer front at Position(ypos=1125)
            show apotheosis pluck onlayer back at Position(ypos=1125)
            with fade
            if persistent.quick_menu:
                $ quick_menu = True
            n "The Princess plucks you from her chest, pinching the scruff of your neck delicately between two fingers as she brings you to eye level.\n"
            voice "audio/_pristine/voice/apotheosis/princess/3.flac"
            show apotheosis pluck talk onlayer back
            with dissolve
            sp "I forgive you your transgressions. But my destiny is inescapable.\n"
            voice "audio/_pristine/voice/apotheosis/contrarian/17.flac"
            show apotheosis pluck onlayer back
            with dissolve
            contrarian "She thinks she's so much better than us! There has to be something else we can do, we're not going out like this.\n"
            voice "audio/_pristine/voice/apotheosis/broken/8.flac"
            broken "She offered us forgiveness. You would turn down such an incredible gift? You would turn away from her glory for something as petty as pride?\n"
            menu:
                extend ""

                "{i}• [[Hurl the blade at her eye.]{/i}":
                    voice "audio/_pristine/voice/apotheosis/contrarian/18.flac"
                    contrarian "Yes. YES! Let's give her something to remember us by.\n"
                    $ blade_held = False
                    $ default_mouse = "$"
                    voice "audio/_pristine/voice/apotheosis/narrator/12.flac"
                    play audio "audio/final/Razor_SwordSwish_1.flac"
                    show knife apotheosis hurl onlayer inyourface at Position(ypos=1125)
                    show player apotheosis hurl onlayer inyourface at Position(ypos=1125)
                    with dissolve
                    n "You concentrate your will to a fine point, and hurl your blade at the Princess' eye. It flies through the night sky and...\n"
                    voice "audio/_pristine/voice/apotheosis/broken/9.flac"
                    broken "And then nothing. She could never be harmed by—\n{w=5.20}{nw}"
                    show screen disableclick(0.5)
                    $ gallery_apotheosis.unlock_item(10)
                    $ renpy.save_persistent()
                    stop music
                    stop music2
                    voice "audio/_pristine/voice/apotheosis/princess/scream1.flac"
                    play audio "audio/one_shot/new/STP_stabcut_1.flac"
                    hide knife onlayer inyourface
                    hide player onlayer inyourface
                    hide farback onlayer farback
                    hide debris onlayer front
                    hide apotheosis onlayer back
                    show farback apotheosis eye out onlayer farback at shakeshort, Position(ypos=1125)
                    show debris apotheosis eye out onlayer front at shakeshort, Position(ypos=1125)
                    show apotheosis eye out onlayer back at shakeshort, Position(ypos=1125)
                    with dissolve
                    sp "AHHHHHHHHHHHHHHHHHH!\n"
                    voice "audio/_pristine/voice/apotheosis/narrator/13b.flac"
                    n "It pierces her cornea.\n"
                    voice "audio/_pristine/voice/apotheosis/narrator/14.flac"
                    play audio "audio/_pristine/sfx/breeze.flac"
                    show debris apotheosis eye out onlayer front at zoom_fall
                    show apotheosis eye out onlayer back at zoom_fall
                    n "She howls, recoiling in pain, and you fall from her distracted hand.\n"
                    $ quick_menu = False
                    play tertiary "audio/one_shot/tackle.flac"
                    queue tertiary "audio/final/Tower_Earthquake_oneshot_faded_1.flac"
                    voice "audio/_pristine/voice/apotheosis/narrator/15.flac"
                    stop sound fadeout 5.0
                    play secondary "audio/_pristine/sfx/Apotheosis Oppresive AMB_2loop.flac" loop
                    hide debris onlayer front
                    hide farback onlayer farback
                    hide apotheosis onlayer back
                    with fade
                    scene bg black
                    with fade
                    scene bg black
                    with fade
                    scene farback apotheosis eye crash onlayer farback at Position(ypos=1125)
                    show debris apotheosis eye crash onlayer front at Position(ypos=1125)
                    show apotheosis eye crash onlayer back at Position(ypos=1125)
                    with fade
                    if persistent.quick_menu:
                        $ quick_menu = True
                    n "You hit the ground with a painful thud. She narrowly misses you as she comes crashing down to her knees.\n"
                    voice "audio/_pristine/voice/apotheosis/princess/4a.flac"
                    show apotheosis eye crash talk onlayer back
                    with Dissolve(0.5)
                    sp "So I've misread you. You are not the willful key that will turn the lock of my liberation. You are an enemy to be smitten by my hand.\n"
                    voice "audio/_pristine/voice/apotheosis/narrator/16.flac"
                    play sound "audio/_pristine/sfx/Apotheosis HiPitch tear_4.flac"
                    queue sound "audio/_pristine/sfx/Apotheosis Oppresive_11.flac"
                    play tertiary "audio/_pristine/sfx/apotheosis_erupt.flac"
                    queue tertiary "audio/final/grey_fire_loop3.ogg" loop
                    show quiet creep1 onlayer farback at Position(ypos=1125)
                    show apotheosis eye beam onlayer back
                    show shine apotheosis eye beam 1 onlayer back at Position(ypos=1125)
                    with Dissolve(1.0)
                    n "The Princess holds up her monumental hand, its glowing palm radiating a blinding light. It grows, and grows, until it's all you can see. And then you erupt, your very soul mere kindling to her light.\n"
                    play audio "audio/_pristine/sfx/Apotheosis Oppresive_12.flac"
                    voice "audio/_pristine/voice/apotheosis/narrator/17b.flac"
                    play sound "audio/_pristine/sfx/Apotheosis Oppresive_7.flac"
                    show shine apotheosis eye beam 2 onlayer front
                    with dissolve
                    n "The inferno incinerates everything that is you, and with it... no. No, that's not right! Why is it hot? I'm not supposed to be able to feel anything oh no, oh no no no no no...\n"
                    voice "audio/_pristine/voice/apotheosis/princess/5.flac"
                    play audio "audio/_pristine/sfx/Apotheosis HiPitch tear_3.flac"
                    show apotheosis eye beam talk onlayer back
                    show shine apotheosis eye beam 3 onlayer inyourface
                    with dissolve
                    sp "You leave me no other choice! Suffer for the crime you have committed against my divine body! ... damnation will purify us both.\n"
                    $ gallery_apotheosis.unlock_item(11)
                    $ renpy.save_persistent()
                    $ quick_menu = False
                    stop music fadeout 10.0
                    stop music2 fadeout 10.0
                    stop sound fadeout 10.0
                    stop secondary fadeout 10.0
                    stop tertiary fadeout 10.0
                    play secondary "audio/_music/mound/The Long Quiet Soft FINAL.ogg" loop fadein 10.0
                    hide debris onlayer front
                    hide apotheosis onlayer back
                    hide farback onlayer farback
                    hide shine onlayer inyourface
                    hide shine onlayer back
                    hide shine onlayer inyourface
                    hide shine onlayer farback
                    hide shine onlayer front
                    hide quiet onlayer farback
                    show farback apotheosis eye post onlayer farback at Position(ypos=1125)
                    show quiet creep3 onlayer farback at Position(ypos=1125)
                    show fore apotheosis eye post onlayer front at Position(ypos=1125)
                    show apotheosis eye post beam onlayer front at Position(ypos=1125)
                    with Dissolve(4.0)
                    if persistent.quick_menu:
                        $ quick_menu = True
                    truth "There is nothing left to burn. Yet still you persist amid a world unraveled.\n"
                    voice "audio/_pristine/voice/apotheosis/princess/6.flac"
                    sp "It's cold now. And I feel... small. I thought I was everything.\n"
                    voice "audio/_pristine/voice/apotheosis/princess/7.flac"
                    show apotheosis eye post beam talk onlayer front
                    with Dissolve(0.5)
                    sp "But I'm no better than you, am I?\n"
                    play audio "audio/final/assorted_Handsgrabbing_BIG_1.flac"
                    hide apotheosis onlayer front
                    hide fore onlayer front
                    show hands apotheosis eye 1 onlayer front at Position(ypos=1125)
                    with Dissolve(1.5)
                    $ renpy.pause(1.0)
                    show hands apotheosis eye 2 onlayer front at Position(ypos=1125)
                    with Dissolve(1.0)
                    $ renpy.pause(0.5)
                    show hands apotheosis eye 3 onlayer front at Position(ypos=1125)
                    with Dissolve(0.5)
                    $ renpy.pause(0.25)
                    show hands apotheosis eye 4 onlayer front at Position(ypos=1125)
                    with Dissolve(0.25)
                    $ renpy.pause(0.125)
                    show hands apotheosis eye 5 onlayer front at Position(ypos=1125)
                    with Dissolve(0.25)
                    $ renpy.pause(0.125)
                    show hands apotheosis eye 6 onlayer front at Position(ypos=1125)
                    with Dissolve(0.25)
                    $ renpy.pause(0.125)
                    show hands apotheosis eye 7 onlayer front at Position(ypos=1125)
                    with Dissolve(0.25)
                    $ renpy.pause(0.125)
                    hide hands onlayer front
                    with Dissolve(0.25)
                    $ renpy.pause(0.125)
                    $ blade_held = False
                    $ default_mouse = "$"
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
                    if loops_finished != 0:
                        truth "You do not get the chance to respond, nor will you ever. It's time to leave. Memory returns.\n"
                    else:
                        truth "You do not get the chance to respond, nor will you ever. Something has taken her away, and it's left something else in her place.\n"
                    $ achievement.grant("ACH_APOTH_BLIND")
                    $ trait_broken = False
                    $ trait_contrarian = False
                    $ apotheosis_end = "defy"
                    $ princess_deny += 1
                    $ princess_kept += 1

                    python:
                        send_heart_location(current_princess)

                    menu:

                        "{i}• [[Approach the mirror.]{/i}":
                            hide mirror onlayer back
                            show content m empty onlayer front at Position(ypos=1125)
                            show mirror frame onlayer front at Position(ypos=1125)
                            with Dissolve(2.0)
                            truth "Silence as you approach. The voices all have burned away.\n"
                            menu:

                                extend ""

                                "{i}• [[Gaze into your reflection.]{/i}":
                                    jump mirror_n_gaze_join



                "{i}• [[Embrace your new goddess.]{/i}":
                    $ apotheosis_contrarian_late_join = False
                    $ apotheosis_contrarian_late_join = True
                    $ blade_held = False
                    $ default_mouse = "$"
                    play audio "audio/final/Tower_WindWHistlingFly_oneshot_1.flac"
                    voice "audio/_pristine/voice/apotheosis/contrarian/20.flac"
                    contrarian "So much for spiting her. Spiting Him it is.\n"
                    voice "audio/_pristine/voice/apotheosis/princess/8a.flac"
                    show apotheosis pluck talk onlayer back
                    with dissolve
                    sp "Good. I can feel your heart opening to mine.\n"
                    #sp "Good. I can feel your heart opening to mine. Here, come to my side.\n"
                    jump apotheosis_contrarian_freedom_join

        "{i}• [[Embrace your new goddess.]{/i}":
            jump apotheosis_pristine_freedom

        "{i}• [[Flee.]{/i}" if contrarian_pristine_apoth_menu_explore:
            # note, paranoid does not present flight as an option
            voice "audio/_pristine/voice/apotheosis/narrator/22.flac"
            $ quick_menu = False
            play tertiary "audio/one_shot/footstep_run_dirt_short.flac"
            queue tertiary "audio/final/den_emerge.flac"
            hide blade onlayer front
            hide player onlayer inyourface
            hide fore onlayer front
            hide mid onlayer back
            hide stars onlayer farback
            with fade
            show farback apotheosis flee onlayer farback at Position(ypos=1125)
            show apotheosis flee debris onlayer front at Position(ypos=1125)
            if persistent.quick_menu:
                $ quick_menu = True
            n "A coward to your core, you turn to flee, leaping from the piece of floating debris and into the empty space beyond where the woods used to be.\n"
            voice "audio/_pristine/voice/apotheosis/contrarian/36.flac"
            contrarian "Nah, this isn't cowardice! This is a calculated move.\n"
            voice "audio/_pristine/voice/apotheosis/narrator/23.flac"
            n "Sure it is.\n"
            voice "audio/_pristine/voice/apotheosis/hero/27.flac"
            hero "Can it be a bit of both? I'd be lying if I said I wasn't a just a little afraid of her.\n"
            voice "audio/_pristine/voice/apotheosis/princess/23.flac"
            sp "Are you so awestruck by my glory that you cannot bear to look at me? I. Think. Not.\n"
            voice "audio/_pristine/voice/apotheosis/narrator/24.flac"
            play audio "audio/one_shot/hard tighten.flac"
            show farback apotheosis flee pluck onlayer farback at Position(ypos=1125)
            show apotheosis flee pluck debris onlayer front at Position(ypos=1125)
            with dissolve
            n "As you fall, a great force pulls at the back of your neck, violently yanking you away from whatever lack of destination you were headed towards.\n"
            voice "audio/_pristine/voice/apotheosis/princess/24.flac"
            show apotheosis flee pluck debris onlayer front at shakeshort
            sp "Now witness me!\n"
            voice "audio/_pristine/voice/apotheosis/broken/28.flac"
            broken "Yes, your grace.\n"
            voice "audio/_pristine/voice/apotheosis/narrator/25.flac"
            $ quick_menu = False
            hide farback onlayer farback
            hide apotheosis onlayer front
            hide farback onlayer farback
            hide debris onlayer inyourface
            hide apotheosis onlayer front
            hide player onlayer inyourface
            scene bg black
            with fade
            show farback apotheosis pluck onlayer farback at Position(ypos=1125)
            show debris apotheosis pluck onlayer front at Position(ypos=1125)
            show apotheosis pluck onlayer back at Position(ypos=1125)
            with fade
            if persistent.quick_menu:
                $ quick_menu = True
            n "She turns you to face her. The scruff of your neck is held firmly between two giant fingers.\n"
            voice "audio/_pristine/voice/apotheosis/hero/28a.flac"
            hero "So much for running away.\n"
            voice "audio/_pristine/voice/apotheosis/princess/3.flac"
            show apotheosis pluck talk onlayer back
            with dissolve
            sp "I forgive you your transgressions. But my destiny is inescapable.\n"
            voice "audio/_pristine/voice/apotheosis/contrarian/37.flac"
            show apotheosis pluck onlayer back
            with dissolve
            contrarian "She's right. We don't even have a weapon. It's over, isn't it?\n"
            voice "audio/_pristine/voice/apotheosis/broken/29.flac"
            broken "And yet, she still extends her mercy. We should do as she says. Why are you all resisting in the first place?\n"
            menu:
                extend ""

                "{i}• [[Embrace your new goddess.]{/i}":
                    $ apotheosis_contrarian_late_join = True
                    $ blade_held = False
                    $ default_mouse = "$"
                    voice "audio/_pristine/voice/apotheosis/contrarian/20.flac"
                    contrarian "So much for spiting her. Spiting Him it is.\n"
                    voice "audio/_pristine/voice/apotheosis/princess/8a.flac"
                    show apotheosis pluck talk onlayer back
                    with dissolve
                    sp "Good. I can feel your heart opening to mine.\n"
                    jump apotheosis_contrarian_freedom_join

label paranoid_pristine_apoth_menu_archipelago:

    menu:

        extend ""

        "{i}• [[Take the blade.]{/i}":
            voice "audio/voices/ch3/apotheosis/hero/11.flac"
            #voice "audio/_pristine/voice/apotheosis/hero/29.flac"
            hero "Yeah. Screw all of this. I'm with you. A real god wouldn't need us as part of her plan.\n"
            #voice "audio/voices/ch3/apotheosis/broken/t2_broken_5.flac"
            voice "audio/_pristine/voice/apotheosis/broken/30.flac"
            broken "You'll never make it to her, and even if you do, what could you possibly hope to accomplish?\n"
            #voice "audio/voices/ch3/apotheosis/hero/12.flac"
            voice "audio/_pristine/voice/apotheosis/hero/30.flac"
            hero "We'll do what we were always supposed to. We'll take this blade and we'll sink it into her heart.\n"
            voice "audio/_pristine/voice/apotheosis/paranoid/16.flac"
            paranoid "Look at the way everything's being flung around her. If we just throw ourselves in her direction... I don't know. Maybe it'll work. If our thoughts are what gave her power, maybe it can cut both ways. Hahahahahahaha. Maybe we can do whatever we want to do! Maybe none of this is real!\n"
            $ blade_held = True
            $ default_mouse = "blade"
            play audio "audio/one_shot/knife_pickup.flac"
            voice "audio/_pristine/voice/apotheosis/narrator/26.flac"
            hide blade onlayer front
            show player normal hold onlayer inyourface at Position(ypos=1125)
            with dissolve
            n "With a forceful tug, you yank the blade out from the tree.\n"
            voice "audio/voices/ch3/apotheosis/narrator/27.flac"
            $ quick_menu = False
            hide player onlayer inyourface
            hide fore onlayer front
            hide mid onlayer back
            hide stars onlayer farback
            show bg impact onlayer back at Position(ypos=1125)
            with dissolve
            n "You close your eyes and take a deep breath, and for a moment, you can feel everything around you, like you're a part of everything and everything is a part of you.\n"
            voice "audio/voices/ch3/apotheosis/narrator/28.flac"
            if persistent.quick_menu:
                $ quick_menu = True
            hide bg onlayer back
            show stars apotheosis charge onlayer farback at Position(ypos=1125)
            show apotheosis charge onlayer back at Position(ypos=1125)
            show fore apotheosis charge onlayer front at Position(ypos=1125)
            show player normal hold onlayer inyourface at Position(ypos=1125)
            with Dissolve(1.0)
            n "And then your eyes open, settling on your target. It's time.\n"
            menu:
                extend ""

                "{i}• [[Embrace your destiny.]{/i}":
                    $ quick_menu = False
                    voice "audio/_pristine/voice/apotheosis/narrator/29.flac"
                    play tertiary "audio/one_shot/footstep_run_dirt_short.flac"
                    queue tertiary "audio/final/den_emerge.flac"
                    hide stars onlayer farback
                    hide apotheosis onlayer back
                    hide fore onlayer front
                    hide player onlayer inyourface
                    with fade
                    show stars apotheosis charge 2 onlayer farback at Position(ypos=1125)
                    show bg apotheosis charge 2 onlayer back at Position(ypos=1125)
                    show apotheosis charge 2 onlayer back at Position(ypos=1125)
                    show fore apotheosis charge 2 onlayer front at Position(ypos=1125)
                    show player normal hold onlayer inyourface at Position(ypos=1125)
                    with fade
                    if persistent.quick_menu:
                        $ quick_menu = True
                    n "You launch yourself towards the Princess. You can feel the pull of her gravity catch you, carrying you from the ground into the violent swirl of her orbit.\n"
                    $ gallery_apotheosis.unlock_item(3)
                    $ renpy.save_persistent()
                    play audio "audio/final/Tower_WindWHistlingFly_oneshot_1.flac"
                    voice "audio/voices/ch3/apotheosis/princess/sp2.flac"
                    hide stars onlayer farback
                    hide apotheosis onlayer back
                    hide fore onlayer front
                    show stars apotheosis charge 3 onlayer farback at Position(ypos=1125)
                    show bg apotheosis charge 3 onlayer back at Position(ypos=1125)
                    show apotheosis charge 3 onlayer back at Position(ypos=1125)
                    show fore apotheosis charge 3 onlayer front at Position(ypos=1125)
                    with Dissolve(2.0)
                    voice "audio/_pristine/voice/apotheosis/princess/25.flac"
                    sp "Even now, you defy me. Do it, then. Show me what you think it takes to end what's destined to end everything.\n"
                    show apotheosis charge 3 onlayer back at Position(ypos=1125)
                    with dissolve
                    #voice "audio/voices/ch3/apotheosis/hero/13.flac"
                    voice "audio/_pristine/voice/apotheosis/hero/31.flac"
                    hero "Yeah. Do it. Show her.\n"
                    menu:
                        extend ""

                        "{i}• [[Assail the unassailable.]{/i}":
                            voice "audio/_pristine/voice/apotheosis/broken/31.flac"
                            broken "You're not going to win. You know that, right? What are you even going to do with that tiny knife? Give her a scratch?\n"
                            voice "audio/_pristine/voice/apotheosis/paranoid/17a.flac"
                            paranoid "Hahahahahahaha. You still don't get it, do you? We can be whatever we want to be. Nothing is real! It all might as well just be a dream.\n"
                            voice "audio/_pristine/voice/apotheosis/hero/32.flac"
                            hero "Are you okay?\n"
                            voice "audio/_pristine/voice/apotheosis/paranoid/18.flac"
                            play audio "audio/_pristine/sfx/breeze.flac"
                            hide player onlayer inyourface
                            hide bg onlayer back
                            hide stars onlayer farback
                            hide apotheosis onlayer back
                            hide fore onlayer front
                            show farback apotheosis paranoid attack 1 onlayer farback at Position(ypos=1125)
                            show debris apotheosis paranoid attack 1 back onlayer back at Position(ypos=1125)
                            show apotheosis paranoid attack 1 onlayer front at Position(ypos=1125)
                            show front apotheosis paranoid attack 1 onlayer inyourface at Position(ypos=1125)
                            with Dissolve(1.0)
                            paranoid "Of course I'm not okay! I've never been okay. But maybe I needed to never be okay for us to make this happen.\n"
                            $ gallery_apotheosis.unlock_item(4)
                            $ renpy.save_persistent()
                            voice "audio/_pristine/voice/apotheosis/narrator/30.flac"
                            play audio "audio/_pristine/sfx/apoth_swing_1.flac"
                            show apotheosis paranoid attack 2 onlayer front at Position(ypos=1125)
                            show front apotheosis paranoid attack 2 onlayer inyourface at Position(ypos=1125)
                            with Dissolve(1.0)
                            n "As you fall towards the Princess, you swing the blade in a massive arc, putting all of your strength behind it. It cuts a shockwave through the very air, splitting everything in its path.\n"
                            #voice "audio/_pristine/voice/apotheosis/hero/33.flac"
                            #hero "I'll be damned. We did that?\n"
                            $ renpy.music.set_volume(0.0, 0.5, channel='music')
                            #voice "audio/_pristine/voice/apotheosis/narrator/31.flac"
                            #play audio "audio/_pristine/sfx/Apotheosis Tentacle feather_5.flac"
                            #play tertiary "audio/_pristine/sfx/Apotheosis HiPitch tear_3.flac"
                            #show farback apotheosis paranoid attack 2 onlayer farback at Position(ypos=1125)
                            #show debris apotheosis paranoid attack 2 back onlayer back at Position(ypos=1125)
                            #show apotheosis paranoid attack 2 onlayer front at Position(ypos=1125)
                            #show front apotheosis paranoid attack 2 onlayer inyourface at Position(ypos=1125)
                            #with Dissolve(1.0)
                            #n "The divine confidence in the Princess' eyes fades as she sees it coming, horror dawning in her expression.\n"
                            voice "audio/_pristine/voice/apotheosis/broken/32.flac"
                            broken "It won't be enough.\n"
                            voice "audio/_pristine/voice/apotheosis/princess/26.flac"
                            show apotheosis paranoid attack 2 talk onlayer front
                            with dissolve
                            sp "Huh. How unexpected.\n"
                            voice "audio/_pristine/voice/apotheosis/narrator/32.flac"
                            play audio "audio/_pristine/sfx/apoth_anime_pew.flac"
                            hide front onlayer inyourface
                            #scene bg impact onlayer inyourface at Position(ypos=1125)
                            #with Dissolve(1.0)
                            #hide bg onlayer inyourface
                            hide apotheosis onlayer front
                            hide debris onlayer back
                            if persistent.flickering:
                                show farback apotheosis paranoid attack dust onlayer farback at shakeshort
                                show apotheosis paranoid attack dust onlayer back at shakeshort, Position(ypos=1125)
                                show debris apotheosis paranoid attack dust onlayer front at shakeshort
                                show player apotheosis paranoid attack dust onlayer inyourface at shakeshort, Position(ypos=1125)
                                with flash
                            else:
                                show farback apotheosis paranoid attack dust onlayer farback at shakeshort
                                show apotheosis paranoid attack dust onlayer back at shakeshort, Position(ypos=1125)
                                show debris apotheosis paranoid attack dust onlayer front at shakeshort
                                show player apotheosis paranoid attack dust onlayer inyourface at shakeshort, Position(ypos=1125)
                                with dissolve
                            n "As the blow lands, the entire world shakes. The outline of the Princess disappears into a storm of dust and debris.\n"
                            play audio "audio/final/Tower_Earthquake_oneshot_faded_1.flac"
                            voice "audio/_pristine/voice/apotheosis/hero/34.flac"
                            hide farback onlayer farback
                            hide apotheosis onlayer back
                            hide debris onlayer front
                            hide player onlayer inyourface
                            show bg impact onlayer farback at shakeshort, Position(ypos=1125)
                            with fade
                            hero "Could we have done that the whole time?!\n"
                            voice "audio/_pristine/voice/apotheosis/broken/33.flac"
                            broken "It was a fluke, I'm sure. An accident. That's all.\n"
                            voice "audio/_pristine/voice/apotheosis/hero/35.flac"
                            hero "It won't be a fluke if we do it again.\n"
                            voice "audio/_pristine/voice/apotheosis/narrator/33.flac"
                            $ renpy.music.set_volume(1.0, 3.5, channel='music')
                            play audio "audio/_pristine/sfx/breeze.flac"
                            hide farback onlayer farback
                            hide apotheosis onlayer front
                            hide debris onlayer back
                            hide player onlayer inyourface
                            show farback apotheosis dust reveal onlayer farback at Position(ypos=1125)
                            show apotheosis dust reveal onlayer back at Position(ypos=1125)
                            show debris apotheosis dust reveal onlayer front at Position(ypos=1125)
                            with Dissolve(2.5)
                            n "As the dust settles, the form of the Princess comes back into view. Her skin and vestments are lightly scuffed, but her body is whole, and her face is full of self-righteous fury.\n"
                            voice "audio/_pristine/voice/apotheosis/hero/36a.flac"
                            hero "At least we made her mad. That has to count for something.\n"
                            #voice "audio/_pristine/voice/apotheosis/hero/36.flac"
                            #hero "Well, at least we made her mad. That means something.\n"
                            # Close the eyes on her dress as well.
                            voice "audio/_pristine/voice/apotheosis/narrator/34.flac"
                            show apotheosis dust reveal close onlayer back with dissolve
                            n "But she holds her anger back. Her eyes close, and a gentle smile curls across her lips.\n"
                            voice "audio/_pristine/voice/apotheosis/princess/27.flac"
                            show apotheosis dust reveal close talk onlayer back with dissolve
                            sp "And so the little bird has found his heart at the end of the world.\n"
                            voice "audio/_pristine/voice/apotheosis/narrator/35.flac"
                            show apotheosis dust reveal open onlayer back with dissolve
                            n "Her eyes flit open, pupils narrowing on your form.\n"
                            voice "audio/_pristine/voice/apotheosis/princess/28.flac"
                            show apotheosis dust reveal open talk onlayer back with dissolve
                            sp "But is it courage that courses through his veins? Or is it madness?\n"
                            #voice "audio/_pristine/voice/apotheosis/princess/29.flac"
                            #sp "So this is the final test before my ascension.\n"
                            voice "audio/_pristine/voice/apotheosis/narrator/36.flac"
                            show apotheosis dust reveal open onlayer back with dissolve
                            n "The world around her stills. The debris stops in place, and the air is calm and silent.\n"
                            voice "audio/_pristine/voice/apotheosis/princess/30.flac"
                            show apotheosis dust reveal open talk onlayer back with dissolve
                            sp "You walk a razor's edge. It won't be long before you slip.\n"
                            $ gallery_apotheosis.unlock_item(5)
                            $ renpy.save_persistent()
                            play tertiary "audio/_pristine/sfx/_rock_storm_3.flac"
                            play audio "audio/_pristine/sfx/Apotheosis HiPitch tear_4.flac"
                            voice "audio/_pristine/voice/apotheosis/narrator/37.flac"
                            if persistent.flickering:
                                hide debris onlayer front
                                hide farback onlayer farback
                                hide apotheosis onlayer back
                                show farback apotheosis paranoid pelt onlayer farback at Position(ypos=1125)
                                show apotheosis paranoid pelt onlayer back at Position(ypos=1125)
                                show debris apotheosis pelt anim onlayer front at Position(ypos=1125)
                                show player apotheosis pelt anim onlayer inyourface at Position(ypos=1125)
                                with flash
                            else:
                                hide debris onlayer front
                                hide farback onlayer farback
                                hide apotheosis onlayer back
                                show farback apotheosis paranoid pelt onlayer farback at Position(ypos=1125)
                                show apotheosis paranoid pelt onlayer back at Position(ypos=1125)
                                show debris apotheosis pelt anim onlayer front at Position(ypos=1125)
                                show player apotheosis pelt anim onlayer inyourface at Position(ypos=1125)
                                with Dissolve(1.0)
                            n "And then, in an instant, it all comes at you. You are pelted with stone after massive stone, even the pebbles slicing through you like bullets. You cannot hope to so much as move as the bombardment continues, your body being destroyed bit by bit, crushed under the mass of wood and rock.\n"
                            voice "audio/_pristine/voice/apotheosis/broken/34.flac"
                            hide farback onlayer farback
                            hide apotheosis onlayer back
                            hide debris onlayer front
                            hide player onlayer inyourface
                            show bg impact onlayer inyourface at Position(ypos=1125)
                            with dissolve
                            broken "It's over. You had your moment, I'll give you that, but that's all it was. Hope it was worth it.\n"
                            voice "audio/_pristine/voice/apotheosis/hero/37.flac"
                            hero "Enough with the 'you's! Whether you like it or not, you're a part of us. Hell, whether I like it or not, you're a part of us. That was your moment, too, and we can have another if we all work together. She's not your perfect goddess. Just look at what she's doing to you, her most loyal servant!\n"
                            voice "audio/_pristine/voice/apotheosis/broken/35.flac"
                            broken "This... isn't very nice. But we did make her angry. Isn't it what we deserve?\n"
                            voice "audio/_pristine/voice/apotheosis/paranoid/19.flac"
                            paranoid "Who deserves something like this? She wants her freedom at the expense of ours, and she's willing to destroy us over and over again if it helps her. What kind of god does that? Stop deluding yourself. If we're going to make this work, all of us need to see the truth!\n"
                            voice "audio/_pristine/voice/apotheosis/broken/36.flac"
                            broken "But... I love her.\n"
                            voice "audio/_pristine/voice/apotheosis/narrator/38.flac"
                            n "And she doesn't love you. She doesn't even know you exist. You are just a tiny part of an obstacle, and she is currently in the process of destroying said obstacle. So I suggest you snap out of it now while you still can.\n"
                            menu:
                                extend ""

                                "{i}• [[Still your doubts.]{/i}":
                                    #voice "audio/_pristine/voice/apotheosis/broken/37.flac"
                                    #broken "Okay... I'm willing to try.\n"
                                    #voice "audio/_pristine/voice/apotheosis/hero/39.flac"
                                    #hero "Glad to hear it. All together now.\n"
                                    #voice "audio/_pristine/voice/apotheosis/paranoid/20.flac"
                                    #paranoid "Right. Remember, the only thing that's real is whatever we believe.\n"
                                    $ default_mouse = "sword"
                                    play tertiary "audio/_pristine/sfx/_rock_storm_3.flac" loop
                                    voice "audio/_pristine/voice/apotheosis/narrator/39.flac"
                                    play audio "audio/_pristine/sfx/apoth_free_rocks.flac"
                                    hide bg onlayer inyourface
                                    if persistent.flickering:
                                        show farback apotheosis paranoid charge onlayer farback at Position(ypos=1125)
                                        show apotheosis paranoid charge onlayer back at Position(ypos=1125)
                                        show debris apotheosis pelt anim onlayer front at Position(ypos=1125)
                                        show player apotheosis paranoid charge onlayer inyourface at Position(ypos=1125)
                                        with flash
                                    else:
                                        show farback apotheosis paranoid charge onlayer farback at Position(ypos=1125)
                                        show apotheosis paranoid charge onlayer back at Position(ypos=1125)
                                        show debris apotheosis pelt anim onlayer front at Position(ypos=1125)
                                        show player apotheosis paranoid charge onlayer inyourface at Position(ypos=1125)
                                        with dissolve
                                    n "All at once, the pressure breaks. You burst through a mountain of debris and straight for the Princess' heart. As you soar towards her the eyes on her vestments open wide, the light of their gaze slowing your pursuit as more and more matter continues to assail you.\n"
                                    voice "audio/_pristine/voice/apotheosis/broken/38.flac"
                                    broken "But it's not enough to stop us, is it? We're going to make it to her.\n"
                                    stop tertiary fadeout 2.0
                                    voice "audio/_pristine/voice/apotheosis/narrator/40.flac"
                                    play audio "audio/final/Assorted_SwordMagicalCut_1.flac"
                                    hide debris onlayer front
                                    show farback apotheosis paranoid charge lift onlayer farback at Position(ypos=1125)
                                    show apotheosis paranoid charge lift onlayer back at Position(ypos=1125)
                                    show player apotheosis paranoid charge lift onlayer inyourface at Position(ypos=1125)
                                    with Dissolve(1.5)
                                    n "You are. As you draw near, you extend your blade, readying a powerful strike. It sings through the air.\n"
                                    voice "audio/_pristine/voice/apotheosis/narrator/41.flac"
                                    play audio "audio/_pristine/sfx/Apotheosis Sword Magic Grind Energy_6.flac"
                                    play tertiary "audio/_pristine/sfx/Apotheosis HiPitch tear_4.flac"
                                    if persistent.flickering:
                                        hide player onlayer inyourface
                                        show farback apotheosis paranoid barrier onlayer farback
                                        show apotheosis paranoid barrier onlayer back
                                        show field apotheosis paranoid barrier onlayer inyourface at Position(ypos=1125)
                                        show sparks apotheosis paranoid barrier onlayer inyourface at Position(ypos=1125)
                                        show player apotheosis paranoid barrier onlayer inyourface at Position(ypos=1125)
                                        with flash
                                    else:
                                        hide player onlayer inyourface
                                        show farback apotheosis paranoid barrier onlayer farback
                                        show apotheosis paranoid barrier onlayer back
                                        show field apotheosis paranoid barrier onlayer inyourface at Position(ypos=1125)
                                        show sparks apotheosis paranoid barrier onlayer inyourface at Position(ypos=1125)
                                        show player apotheosis paranoid barrier onlayer inyourface at Position(ypos=1125)
                                        with Dissolve(1.0)
                                    n "And is met with a barrier of light. You remain frozen in midair, the two of you unblinking, waiting to see who breaks first.\n"
                                    voice "audio/_pristine/voice/apotheosis/hero/40.flac"
                                    hero "And then we win... right?\n"
                                    voice "audio/_pristine/voice/apotheosis/paranoid/21.flac"
                                    paranoid "That's what should happen. Why isn't it happening? Did we do something wrong? Were all these powerful, heroic thoughts not enough?\n"
                                    voice "audio/_pristine/voice/apotheosis/broken/39.flac"
                                    broken "I believe! I believe in us! Isn't that enough?\n"
                                    voice "audio/_pristine/voice/apotheosis/paranoid/22a.flac"
                                    paranoid "Unless we got the rules wrong... I'm sorry. I think I messed this up.\n"
                                    $ paranoid_apotheosis_fight_back = False

                                    # CONSIDERING just making this yet another one option menu where you can only successfully fight back — I don't think giving up here really adds anything, but it also feels like there's been too little room for player agency in this route.
                                    menu:

                                        extend ""

                                        "{i}• (Explore) Then what do we do? I thought you said that all of this was like a dream. That we could choose how it goes. So why can't we choose to win?{/i}":
                                            $ default_mouse = "blade"
                                            #voice "audio/_pristine/voice/apotheosis/hero/43.flac"
                                            #hero "It can't be! I thought you said that all of this was like a dream! That we could choose how it goes.\n"
                                            voice "audio/_pristine/voice/apotheosis/paranoid/25.flac"
                                            play audio "audio/_pristine/sfx/Apotheosis Oppresive_12.flac"
                                            hide sparks onlayer inyourface
                                            hide field onlayer inyourface
                                            show farback apotheosis barrier plummet onlayer farback
                                            show apotheosis barrier plummet onlayer back
                                            show player normal hold onlayer inyourface
                                            with Dissolve(1.0)
                                            paranoid "The thing with dreams is that they always end.\n"
                                            voice "audio/_pristine/voice/apotheosis/princess/34.flac"
                                            show apotheosis barrier plummet talk onlayer back
                                            with dissolve
                                            sp "An admirable effort, but one that would never have succeeded. Come. Let us leave this world of illusions.\n"
                                            voice "audio/_pristine/voice/apotheosis/narrator/45.flac"
                                            n "She's just trying to undermine you. She's lying, don't listen to her—\n{w=4.5}{nw}"
                                            show screen disableclick(0.5)
                                            $ renpy.music.set_volume(0.5, 0.75, channel='music')
                                            $ blade_held = False
                                            $ default_mouse = "$"
                                            stop sound fadeout 10.0
                                            stop secondary fadeout 10.0
                                            stop tertiary fadeout 10.0
                                            play secondary "audio/_music/mound/The Long Quiet Soft FINAL.ogg" loop fadein 10.0
                                            show farback quiet onlayer farback
                                            show apotheosis paranoid quiet begin onlayer back
                                            show player apotheosis paranoid quiet begin onlayer inyourface
                                            with Dissolve(1.0)
                                            truth "But before He can finish His thought, He is gone, and your blade has vanished from your hand. The world around you unravels into a textured nothing.\n"
                                            voice "audio/_pristine/voice/apotheosis/princess/35.flac"
                                            hide player onlayer inyourface
                                            show apotheosis paranoid quiet begin talk onlayer back
                                            with Dissolve(1.0)
                                            sp "You have no weapon. Your will has been conquered.\n"

                                        "{i}• No! We just have to push harder! We wouldn't be here if there wasn't a way for us to win.{/i}":
                                            $ paranoid_apotheosis_fight_back = True
                                            voice "audio/_pristine/voice/apotheosis/hero/41.flac"
                                            hero "That's right! So come on, push! All of you!\n"
                                            voice "audio/_pristine/voice/apotheosis/broken/40.flac"
                                            broken "I'll do my best!\n"
                                            voice "audio/_pristine/voice/apotheosis/paranoid/23.flac"
                                            paranoid "All right. One. Last. Try.\n"
                                            voice "audio/_pristine/voice/apotheosis/narrator/42.flac"
                                            play audio "audio/_pristine/sfx/Apotheosis Sword Magic Grind Energy_4.flac"
                                            show field apotheosis paranoid barrier onlayer inyourface at shakeshort, Position(ypos=1125)
                                            show sparks apotheosis paranoid barrier onlayer inyourface at shakeshort,  Position(ypos=1125)
                                            show player apotheosis paranoid barrier onlayer inyourface at shakeshort,  Position(ypos=1125)
                                            n "You continue the struggle, your blade kicking up sparks as it grinds against the Princess' barrier. But you're getting to her.\n"
                                            voice "audio/_pristine/voice/apotheosis/princess/31.flac"
                                            show apotheosis paranoid barrier talk onlayer back
                                            with dissolve
                                            sp "Your persistence is admirable, but it's misplaced.\n"
                                            voice "audio/_pristine/voice/apotheosis/broken/41.flac"
                                            show apotheosis paranoid barrier onlayer back
                                            with dissolve
                                            broken "We're so much more than I thought we were... it won't be misplaced if we win!\n"
                                            $ gallery_apotheosis.unlock_item(6)
                                            $ renpy.save_persistent()
                                            voice "audio/_pristine/voice/apotheosis/narrator/43.flac"
                                            play audio "audio/_pristine/sfx/Apotheosis Sword Magic Grind Energy_10.flac"
                                            play tertiary "audio/_pristine/sfx/Apotheosis Sword Magic Grind Energy_3.flac"
                                            play secondary "audio/_pristine/sfx/barrier_break.flac"
                                            show sparks apotheosis paranoid barrier onlayer inyourface at shakeshort,  Position(ypos=1125)
                                            show player apotheosis paranoid barrier onlayer inyourface at shakeshort,  Position(ypos=1125)
                                            show field apotheosis shatter anim onlayer inyourface at shakeshort
                                            n "You ignore the Princess' words and push a little further, and then... a crack. And where that crack formed, another forms, and then another. Finally, it shatters.\n"
                                            voice "audio/_pristine/voice/apotheosis/hero/42.flac"
                                            hide sparks onlayer inyourface
                                            hide field onlayer inyourface
                                            with dissolve
                                            hero "We did it! We actually did it!\n"
                                            voice "audio/_pristine/voice/apotheosis/narrator/44.flac"
                                            play audio "audio/final/Assorted_SwordMagicalCut_2.flac"
                                            show farback apotheosis barrier plummet onlayer farback
                                            show apotheosis barrier plummet onlayer back
                                            show player apotheosis barrier plummet onlayer inyourface
                                            with Dissolve(1.0)
                                            n "The Princess' face remains serene as your blade plummets towards her heart.\n"
                                            voice "audio/_pristine/voice/apotheosis/princess/32.flac"
                                            show apotheosis barrier plummet talk onlayer back
                                            with dissolve
                                            sp "A victory, but one that remains rooted in the material. And I am beyond that now. Come. Let us leave this world of illusions.\n"
                                            $ renpy.music.set_volume(0.5, 0.75, channel='music')
                                            $ default_mouse = "$"
                                            $ blade_held = False
                                            stop sound fadeout 10.0
                                            stop secondary fadeout 10.0
                                            stop tertiary fadeout 10.0
                                            play secondary "audio/_music/mound/The Long Quiet Soft FINAL.ogg" loop fadein 10.0
                                            show farback quiet onlayer farback
                                            show apotheosis paranoid quiet begin onlayer back
                                            show player apotheosis paranoid quiet begin onlayer inyourface
                                            with Dissolve(2.0)
                                            truth "Before your blade can pierce her heart, it is vanished from your hand. The world around you unravels into a textured nothing.\n"
                                            $ achievement.grant("ACH_APOTH_BATTLE")
                                            voice "audio/_pristine/voice/apotheosis/princess/33.flac"
                                            hide player onlayer inyourface
                                            show apotheosis paranoid quiet begin talk onlayer back
                                            with Dissolve(1.0)
                                            sp "You have no weapon. Our battle is at an end.\n"
                                            #voice "audio/_pristine/voice/apotheosis/paranoid/24.flac"
                                            #paranoid "We didn't do that, did we? Maybe we're less in control here than I thought.\n"
                                            #voice "audio/_pristine/voice/apotheosis/paranoid/25.flac"
                                            #paranoid "The thing with dreams is that they always end.\n"



                                    voice "audio/_pristine/voice/apotheosis/broken/42.flac"
                                    show apotheosis paranoid quiet begin onlayer back
                                    with dissolve
                                    broken "Is she going to hurt us now?\n"
                                    #voice "audio/_pristine/voice/apotheosis/princess/36.flac"
                                    #sp "But it means something that you and I persist while nothing else does.\n"
                                    $ gallery_apotheosis.unlock_item(8)
                                    $ renpy.save_persistent()
                                    play audio "audio/_pristine/sfx/Apotheosis Tentacle feather_1.flac"
                                    scene reality ending
                                    hide apotheosis onlayer farback
                                    hide farback onlayer farback
                                    hide bg onlayer farback
                                    show apotheosis reach onlayer back
                                    show debris apotheosis reach onlayer front
                                    with Dissolve(1.5)
                                    truth "The Princess reaches forward into the textured nothing and buries her fingers in its divine flesh. Her touch is soft.\n"
                                    voice "audio/_pristine/voice/apotheosis/broken/43.flac"
                                    broken "Oh... that feels nice.\n"
                                    #voice "audio/_pristine/voice/apotheosis/hero/44.flac"
                                    #hero "Come on now, I know it feels easy to give up at a time like this, but there has to be something we can do.\n"
                                    #voice "audio/_pristine/voice/apotheosis/princess/37.flac"
                                    #sp "All that remains is for me to pull at the seams.\n"
                                    voice "audio/_pristine/voice/apotheosis/princess/12a.flac"
                                    show apotheosis reach talk onlayer back
                                    with dissolve
                                    sp "The flame may be snuffed, but the wall remains. This isn't just for my glory. You are a part of this now.\n"
                                    $ default_mouse = "eye"
                                    $ renpy.music.set_volume(0.0, 0.75, channel='music')
                                    $ renpy.music.set_volume(1.0, 0.75, channel='music2')
                                    play audio "audio/final/Assorted_TapestyUnraveledBreakingRip_1.flac"
                                    play sound "audio/_pristine/sfx/Apotheosis HiPitch tear_3.flac"
                                    show apotheosis tear onlayer back
                                    $ renpy.pause(0.75)
                                    hide apotheosis onlayer back
                                    hide debris onlayer front
                                    scene bg black
                                    show bg black onlayer farback
                                    show apotheosis darkness 1 onlayer front at Position(ypos=1125)
                                    truthmid "Her grip tightens, and somehow, you feel it. The pain sits at the limits of your comprehension. Like an endless sea of hands falling on you one after another after another before finally collapsing in on themselves. You lose yourself in the darkness.\n"
                                    voice "audio/_pristine/voice/apotheosis/broken/44.flac"
                                    broken "She's hurting us again. I've never hurt like this before.\n"
                                    voice "audio/_pristine/voice/apotheosis/hero/45.flac"
                                    hero "She isn't even touching us. How can she hurt us without touching us...?\n"
                                    voice "audio/_pristine/voice/apotheosis/paranoid/26.flac"
                                    paranoid "Unless all of this is us. No. No, we can't be this. But it feels like she's ripping us apart.\n"
                                    menu:
                                        extend ""

                                        "{i}• [[Fight back.]{/i}":
                                            voice "audio/_pristine/voice/apotheosis/paranoid/27.flac"
                                            paranoid "Maybe... maybe if we feel all of this nothing... maybe we can use it.\n"
                                            voice "audio/_pristine/voice/apotheosis/hero/46.flac"
                                            hero "Anything to make this stop!\n"
                                            voice "audio/_pristine/voice/apotheosis/broken/45.flac"
                                            broken "Anything to make her feel what we feel.\n"
                                            if paranoid_apotheosis_fight_back == False:
                                                jump apotheosis_tendrils_shared_join
                                            else:
                                                $ renpy.music.set_volume(1.0, 0.0, channel='music')
                                                $ renpy.music.set_volume(0.0, 0.0, channel='music2')
                                                stop music
                                                stop music2
                                                play sound "audio/_pristine/sfx/Apotheosis Tentacle feather_5.flac"
                                                show apotheosis darkness 5 onlayer front
                                                with dissolve
                                                truth "You are a wave of tendrils racing against themselves and down the shape of an arm. You snap around it.\n"
                                                play sound "audio/_pristine/sfx/apoth_snap.flac"
                                                $ quick_menu = False
                                                voice "audio/_pristine/voice/apotheosis/princess/scream2.flac"
                                                show apotheosis darkness 4 onlayer front
                                                spmid "AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH!\n"
                                                voice "audio/_pristine/voice/apotheosis/broken/46a.flac"
                                                broken "But that isn't enough, is it? We can show her more... we can show her what she's done to us! We can make her understand. We can make her feel what we've felt.\n"
                                                play audio "audio/_pristine/sfx/Apotheosis HiPitch tear_3.flac"
                                                show apotheosis paranoid torment 1 onlayer front
                                                with Dissolve(1.5)
                                                truth "Your awareness shifts between undulating fibers of nothingness that is somehow outside of your body, but part of it. Time yields to feeling.\n"
                                                play audio "audio/_pristine/sfx/Apotheosis Tentacle feather_5.flac"
                                                show apotheosis paranoid torment 2 onlayer front
                                                with Dissolve(1.0)
                                                truth "You wrap around wrist, ankle, neck, and pull from her heart the whole of her experience, and in return, she pulls from your heart the whole of yours.\n"
                                                play audio "audio/_pristine/sfx/Apotheosis Oppresive_12.flac"
                                                show apotheosis paranoid torment 3 onlayer front
                                                with Dissolve(1.0)
                                                truth "So much of her is empty bluster. Boasts muttered first in quiet to give an empty life a sense of meaning, and then the same boasts wrapped in a bow of true belief.\n"
                                                play audio "audio/one_shot/hard tighten.flac"
                                                show apotheosis paranoid torment 4 onlayer front
                                                with Dissolve(1.0)
                                                truth "Belief turned to arrogance. Arrogance that shatters as she finally sees something other than herself.\n"
                                                voice "audio/_pristine/voice/apotheosis/princess/39.flac"
                                                show apotheosis paranoid torment 4 talk onlayer front
                                                with Dissolve(1.0)
                                                sp "Oh. We've both hurt each other so very much, haven't we?\n"
                                                $ gallery_apotheosis.unlock_item(7)
                                                $ renpy.save_persistent()
                                                play sound "audio/final/Assorted_TapestyUnraveledBreakingRip_2.flac"
                                                play audio "audio/_pristine/sfx/Fury Body Horror_1.flac"
                                                $ quick_menu = False
                                                hide apotheosis onlayer front
                                                with fade
                                                show farback quiet onlayer farback at Position(ypos=1125)
                                                show apotheosis paranoid torment final quiet onlayer back at Position(ypos=1125)
                                                with fade
                                                if persistent.quick_menu:
                                                    $ quick_menu = True
                                                truth "Your eyes open. She is bound to you, and you are bound to her. Hollow echoes of what you used to be.\n"
                                                voice "audio/_pristine/voice/apotheosis/princess/40.flac"
                                                show apotheosis paranoid torment final talk onlayer back
                                                with dissolve
                                                sp "I can hear your voices prattle in my head. I was never going to ascend. This is all so very small. I'm so very small. I'm sorry.\n"
                                                play audio "audio/final/assorted_Handsgrabbing_BIG_1.flac"
                                                hide apotheosis onlayer back
                                                hide fore onlayer front
                                                show hands apotheosis paranoid onlayer back at Position(ypos=1125)
                                                with Dissolve(1.5)
                                                $ renpy.pause(1.0)
                                                show hands apotheosis paranoid 2 onlayer back at Position(ypos=1125)
                                                with Dissolve(1.0)
                                                $ renpy.pause(0.5)
                                                show hands apotheosis paranoid 3 onlayer back at Position(ypos=1125)
                                                with Dissolve(0.5)
                                                $ renpy.pause(0.25)
                                                show hands apotheosis paranoid 4 onlayer back at Position(ypos=1125)
                                                with Dissolve(0.25)
                                                $ renpy.pause(0.125)
                                                show hands apotheosis paranoid 5 onlayer back at Position(ypos=1125)
                                                with Dissolve(0.25)
                                                $ renpy.pause(0.125)
                                                show hands apotheosis paranoid 6 onlayer back at Position(ypos=1125)
                                                with Dissolve(0.25)
                                                $ renpy.pause(0.125)
                                                hide hands onlayer back
                                                with Dissolve(0.25)
                                                $ renpy.pause(0.125)
                                                $ blade_held = False
                                                $ default_mouse = "$"
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
                                                if loops_finished != 0:
                                                    truth "But you do not get the chance to respond, nor will you ever. It's time to leave. Memory returns.\n"
                                                else:
                                                    truth "But you do not get the chance to respond, nor will you ever. Something has taken her away, and it's left something else in her place.\n"
                                                $ achievement.grant("ACH_APOTH_THREADS")
                                                $ trait_broken = False
                                                $ trait_paranoid = False
                                                $ apotheosis_end = "unraveled"
                                                $ princess_deny += 1
                                                $ princess_kept += 1

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
                                                                jump mirror_n_gaze_join
                                                # END

                                        "{i}• [[Submit.]{/i}":
                                            voice "audio/_pristine/voice/apotheosis/princess/41.flac"
                                            sp "Finally you have seen my light. All is forgiven.\n"
                                            jump apotheosis_alone_final_join

        "{i}• [[Embrace your new goddess.]{/i}":
            jump apotheosis_pristine_freedom
