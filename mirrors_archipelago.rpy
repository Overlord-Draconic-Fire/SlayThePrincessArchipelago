# Archipelago Override: Mirror Labels
# These labels are overridden from game/scripts/special/mirror/mirror_intro_join.rpy
# They allow us to hook into Archipelago logic without modifying the original game files.

label mirror_start_2_archipelago:
    python:
        try:
            from CURRENT_PRINCESS_TO_LOCATION import CURRENT_PRINCESS_TO_LOCATION
            
            # Appeler send_location avec la location correspondante
            if archipelago_client and current_princess in CURRENT_PRINCESS_TO_LOCATION:
                location_name = CURRENT_PRINCESS_TO_LOCATION[current_princess]
                archipelago_client.send_location(location_name)
            elif archipelago_client:
                renpy.log(f"[AP] current_princess '{current_princess}' non mappé dans CURRENT_PRINCESS_TO_LOCATION")
        except Exception as e:
            renpy.log(f"[AP] Erreur lors de l'envoi de location: {e}")

    if current_run_mirror_comment or current_run_mirror_touched:
        voice "audio/voices/mirror/intro/hero/3.flac"
        hero "And there's that mirror again. Why is it here? Why now?!\n"
    else:
        voice "audio/voices/mirror/intro/hero/4.flac"
        hero "And is that a... mirror? Why is it here? Why now?!\n"

    default mirror_comfort_count = 0
    if loops_finished == 0:
        default mirror_1_where_princess = False
        default mirror_1_narrator_gone = False
        default mirror_1_mirror_suggest = False
        $ mirror_hero_scared_flag = True
        label mirror_1_menu:
            menu:
                extend ""

                "{i}• (Explore) I don't know where she went, and I don't know how we'd even go about looking for her.{/i}" if mirror_1_where_princess == False:
                    $ mirror_1_where_princess = True
                    if trait_skeptic:
                        voice "audio/voices/mirror/intro/skeptic/2.flac"
                        skeptic "If there's even a her to find anymore.\n"
                    if trait_opportunist:
                        voice "audio/voices/mirror/intro/opportunist/2.flac"
                        opportunist "Does this mean we won?\n"
                    voice "audio/voices/mirror/intro/hero/5.flac"
                    hero "You're right. She's gone. It's just us and that... awful thing.\n"
                    if trait_stubborn:
                        voice "audio/voices/mirror/intro/stubborn/2.flac"
                        stubborn "It's like it's mocking us.\n"
                    if trait_hunted:
                        voice "audio/voices/mirror/intro/hunted/2.flac"
                        hunted "Let's just stay still.\n"
                    if trait_smitten:
                        voice "audio/voices/mirror/intro/smitten/2.flac"
                        smitten "I can't believe she was taken away from us! The nerve.\n"
                    if trait_paranoid and current_princess != "happy":
                        voice "audio/voices/mirror/intro/paranoid/2.flac"
                        paranoid "I should feel better with her gone, but I don't.\n"
                    if trait_cheated:
                        voice "audio/voices/mirror/intro/cheated/2.flac"
                        cheated "We just can't win.\n"
                    if trait_cold:
                        voice "audio/voices/mirror/intro/cold/2.flac"
                        cold "Don't bother looking for her. I'm sure it's just a waste of time.\n"
                    if trait_broken:
                        voice "audio/voices/mirror/intro/broken/2.flac"
                        broken "I feel anxious. Does anyone else feel anxious?\n"
                    if trait_contrarian:
                        if mirror_1_narrator_gone == False:
                            voice "audio/voices/mirror/intro/contrarian/2.flac"
                            contrarian "Then what the hell are we supposed to do?\n"
                        else:
                            voice "audio/voices/mirror/intro/contrarian/3a.flac"
                            contrarian "Again, what the hell are we supposed to do?\n"
                    jump mirror_1_menu

                "{i}• (Explore) The Narrator is gone...{/i}" if mirror_1_narrator_gone == False and current_princess != "happy":
                    $ mirror_1_narrator_gone = True
                    voice "audio/voices/mirror/intro/hero/6.flac"
                    hero "He is. Does that mean the world ended?\n"
                    if trait_skeptic:
                        voice "audio/voices/mirror/intro/skeptic/3a.flac"
                        skeptic "It must have. Do any of us know what the world ending is supposed to look like?\n"
                    if trait_hunted:
                        voice "audio/voices/mirror/intro/hunted/3.flac"
                        hunted "It hasn't ended. We're still here.\n"
                    if trait_cold:
                        voice "audio/voices/mirror/intro/cold/3.flac"
                        cold "He was never going to outlast us.\n"
                    if trait_contrarian:
                        if mirror_1_where_princess == False:
                            voice "audio/voices/mirror/intro/contrarian/3.flac"
                            contrarian "What are we supposed to do now?\n"
                        else:
                            voice "audio/voices/mirror/intro/contrarian/3a.flac"
                            contrarian "Again, what the hell are we supposed to do?\n"
                    if trait_paranoid:
                        voice "audio/voices/mirror/intro/paranoid/3.flac"
                        paranoid "Yeah. No voice needling us anymore. Feels good, but I also feel... itchy. Cold.\n"
                    if trait_stubborn:
                        voice "audio/voices/mirror/intro/stubborn/3.flac"
                        stubborn "The world didn't end. We're still here. Come on, we just need to keep going!\n"
                    if trait_broken:
                        voice "audio/voices/mirror/intro/broken/3.flac"
                        broken "Figures the world would end and leave us with all this nothing.\n"
                    if trait_opportunist:
                        voice "audio/voices/mirror/intro/opportunist/3.flac"
                        opportunist "We're top of the pecking order now... right, boys?\n"
                    if trait_smitten:
                        voice "audio/voices/mirror/intro/smitten/3.flac"
                        smitten "A villain vanquished.\n"
                    if trait_cheated:
                        voice "audio/voices/mirror/intro/cheated/3.flac"
                        cheated "Good riddance.\n"
                    jump mirror_1_menu

                "{i}• (Explore) I think I'm supposed to look at the mirror.{/i}" if mirror_1_mirror_suggest == False:
                    $ mirror_1_mirror_suggest = True
                    $ mirror_n_explore = True
                    voice "audio/voices/mirror/intro/hero/7.flac"
                    hero "There's something dreadful about it. I don't think you should.\n"
                    if trait_contrarian:
                        voice "audio/voices/mirror/intro/contrarian/4.flac"
                        contrarian "No. Don't do that.\n"
                    if trait_hunted:
                        voice "audio/voices/mirror/intro/hunted/4.flac"
                        hunted "That thing reeks of death.\n"
                    if trait_paranoid:
                        voice "audio/voices/mirror/intro/paranoid/4.flac"
                        paranoid "It's calling us. And not in a good way.\n"
                    if trait_skeptic:
                        voice "audio/voices/mirror/intro/skeptic/4.flac"
                        skeptic "You're right. Part of me wants the truth, but something stronger is holding me back. Fear.\n"
                    if trait_stubborn:
                        voice "audio/voices/mirror/intro/stubborn/4.flac"
                        stubborn "Screw the mirror! We just need to find the Princess.\n"
                    if trait_broken:
                        voice "audio/voices/mirror/intro/broken/4.flac"
                        broken "I don't want to look at us.\n"
                    if trait_smitten:
                        voice "audio/voices/mirror/intro/smitten/4.flac"
                        smitten "Yes, I fear that we won't like what we'll see. What if we just sit here and preen for a while? That can't hurt, right?\n"
                    if trait_cheated:
                        voice "audio/voices/mirror/intro/cheated/4.flac"
                        cheated "It's going to do something to us. I can feel it.\n"
                    if trait_opportunist:
                        if current_princess == "witch" or current_princess == "happy" or current_princess == "happydry" or current_princess == "dragon" or current_princess == "dragonfused" or current_princess == "dragonhand":
                            voice "audio/voices/mirror/intro/opportunist/4.flac"
                            opportunist "If he thinks it's bad, I'm with him.\n"
                        else:
                            voice "audio/voices/mirror/intro/opportunist/4a.flac"
                            opportunist "If they think it's bad, I'm with them.\n"
                    if trait_cold:
                        if current_princess == "spectre":
                            voice "audio/voices/mirror/intro/cold/4.flac"
                            cold "Ignore him. You have to look.\n"
                        else:
                            voice "audio/voices/mirror/intro/cold/5.flac"
                            cold "Ignore the cowards. You have to look.\n"
                    jump mirror_1_menu

                "{i}• [[Approach the mirror.]{/i}":
                    voice "audio/voices/mirror/intro/hero/8.flac"
                    hero "I'm begging you, don't do this.\n"
                    menu:
                        extend ""

                        "{i}• (Explore) The mirror never scared you before.{/i}" if current_run_mirror_comment or current_run_mirror_touched:
                            $ mirror_n_explore = True
                            voice "audio/voices/mirror/intro/hero/9.flac"
                            hero "It's different now! It feels... I don't know. Final.\n"
                            if mirror_1_mirror_suggest == False:
                                $ mirror_1_mirror_suggest
                                if trait_contrarian:
                                    voice "audio/voices/mirror/intro/contrarian/5.flac"
                                    contrarian "Yeah, don't look at it. I don't like that {i}thing{/i}.\n"
                                if trait_hunted:
                                    voice "audio/voices/mirror/intro/hunted/4.flac"
                                    hunted "That thing reeks of death.\n"
                                if trait_paranoid:
                                    voice "audio/voices/mirror/intro/paranoid/4.flac"
                                    paranoid "It's calling us. And not in a good way.\n"
                                if trait_skeptic:
                                    voice "audio/voices/mirror/intro/skeptic/4.flac"
                                    skeptic "You're right. Part of me wants the truth, but something stronger is holding me back. Fear.\n"
                                if trait_stubborn:
                                    voice "audio/voices/mirror/intro/stubborn/4.flac"
                                    stubborn "Screw the mirror! We just need to find the Princess.\n"
                                if trait_broken:
                                    voice "audio/voices/mirror/intro/broken/4.flac"
                                    broken "I don't want to look at us.\n"
                                if trait_smitten:
                                    voice "audio/voices/mirror/intro/smitten/4.flac"
                                    smitten "Yes, I fear that we won't like what we'll see. What if we just sit here and preen for a while? That can't hurt, right?\n"
                                if trait_cheated:
                                    voice "audio/voices/mirror/intro/cheated/4.flac"
                                    cheated "It's going to do something to us. I can feel it.\n"
                                if trait_opportunist:
                                    if current_princess == "witch" or current_princess == "happy" or current_princess == "happydry":
                                        voice "audio/voices/mirror/intro/opportunist/4.flac"
                                        opportunist "If he thinks it's bad, I'm with him.\n"
                                    else:
                                        voice "audio/voices/mirror/intro/opportunist/4a.flac"
                                        opportunist "If they think it's bad, I'm with them.\n"
                                if trait_cold:
                                    if current_princess == "spectre":
                                        voice "audio/voices/mirror/intro/cold/4.flac"
                                        cold "Ignore him. You have to look.\n"
                                    else:
                                        voice "audio/voices/mirror/intro/cold/5.flac"
                                        cold "Ignore the cowards. You have to look.\n"
                                jump mirror_approach_join

                        "{i}• [[Ignore him.]{/i}":
                            jump mirror_approach_join

    else:
        label mirror_n_menu:
            default mirror_n_cruel_count = 0
            default mirror_n_explore = False
            default mirror_n_silence_flag = False
            default nightmare_2_finished = False
            default mirror_hero_scared_flag = False
            menu:
                extend ""

                "{i}• (Explore) Of course you're scared. This is the end, for you. But it's not the end for me.{/i}" if mirror_n_explore == False:
                    $ mirror_n_explore = True
                    jump mirror_n_cruel

                "{i}• (Explore) It's going to be okay. Just trust me.{/i}" if mirror_n_explore == False and mirror_hero_scared_flag == False:
                    $ mirror_hero_scared_flag = True
                    jump mirror_n_explore_join


                "{i}• (Explore) It's going to be okay. Just trust me. We've been here before, and you always get scared.{/i}" if mirror_n_explore == False and mirror_hero_scared_flag:
                    label mirror_n_explore_join:
                        $ mirror_n_explore = True
                        voice "audio/voices/mirror/intro/hero/10.flac"
                        hero "But it feels so bad! Like looking into it right now is going to be the end of everything.\n"
                        if trait_contrarian:
                            voice "audio/voices/mirror/intro/contrarian/5.flac"
                            contrarian "Yeah, don't look at it. I don't like that {i}thing{/i}.\n"
                        if trait_hunted:
                            voice "audio/voices/mirror/intro/hunted/4.flac"
                            hunted "That thing reeks of death.\n"
                        if trait_paranoid:
                            voice "audio/voices/mirror/intro/paranoid/4.flac"
                            paranoid "It's calling us. And not in a good way.\n"
                        if trait_skeptic:
                            voice "audio/voices/mirror/intro/skeptic/4.flac"
                            skeptic "You're right. Part of me wants the truth, but something stronger is holding me back. Fear.\n"
                        if trait_stubborn:
                            voice "audio/voices/mirror/intro/stubborn/4.flac"
                            stubborn "Screw the mirror! We just need to find the Princess.\n"
                        if trait_broken:
                            voice "audio/voices/mirror/intro/broken/4.flac"
                            broken "I don't want to look at us.\n"
                        if trait_smitten:
                            voice "audio/voices/mirror/intro/smitten/4.flac"
                            smitten "Yes, I fear that we won't like what we'll see. What if we just sit here and preen for a while? That can't hurt, right?\n"
                        if trait_cheated:
                            voice "audio/voices/mirror/intro/cheated/4.flac"
                            cheated "It's going to do something to us. I can feel it.\n"
                        if trait_opportunist:
                            if current_princess == "witch" or current_princess == "happy" or current_princess == "happydry":
                                voice "audio/voices/mirror/intro/opportunist/4.flac"
                                opportunist "If he thinks it's bad, I'm with him.\n"
                            else:
                                voice "audio/voices/mirror/intro/opportunist/4a.flac"
                                opportunist "If they think it's bad, I'm with them.\n"
                        if trait_cold:
                            if current_princess == "spectre":
                                voice "audio/voices/mirror/intro/cold/6.flac"
                                cold "You don't need to comfort him.\n"
                            else:
                                voice "audio/voices/mirror/intro/cold/7.flac"
                                cold "You don't need to comfort them.\n"
                        label mirror_n_menu_comfort:
                            menu:
                                extend ""

                                "{i}• It's not the end. Whatever's on the other side is going to be nice.{/i}":
                                    label mirror_n_comfort_join:
                                        $ mirror_comfort_count += 1
                                        voice "audio/voices/mirror/intro/hero/11.flac"
                                        hero "Okay. If you say so, we'll trust you.\n"
                                        if trait_paranoid:
                                            voice "audio/voices/mirror/intro/paranoid/5.flac"
                                            paranoid "Can we trust you?\n"
                                        if trait_hunted:
                                            voice "audio/voices/mirror/intro/hunted/5.flac"
                                            hunted "I'd like to be somewhere nice.\n"
                                        if trait_stubborn:
                                            voice "audio/voices/mirror/intro/stubborn/5.flac"
                                            stubborn "Maybe there'll be a good fight there. Maybe we'll find her again.\n"
                                        if trait_broken:
                                            voice "audio/voices/mirror/intro/broken/5.flac"
                                            broken "A mercy.\n"
                                        if trait_contrarian:
                                            voice "audio/voices/mirror/intro/contrarian/6.flac"
                                            contrarian "You're not messing with us, right?\n"
                                        if trait_cheated:
                                            voice "audio/voices/mirror/intro/cheated/5a.flac"
                                            cheated "So this is all going to work out?\n"
                                        if trait_skeptic:
                                            voice "audio/voices/mirror/intro/skeptic/5.flac"
                                            skeptic "Feels too good to be true.\n"
                                        if trait_smitten:
                                            voice "audio/voices/mirror/intro/smitten/5.flac"
                                            smitten "She'll be there waiting for us, I just know it.\n"
                                        if trait_opportunist:
                                            voice "audio/voices/mirror/intro/opportunist/5.flac"
                                            opportunist "Finally. We're going places.\n"
                                        if trait_cold:
                                            voice "audio/voices/mirror/intro/cold/8.flac"
                                            cold "Whatever makes you happy.\n"
                                        jump mirror_n_menu

                                "{i}• It's the end for you, but not for me.{/i}":
                                    label mirror_n_cruel:
                                        $ mirror_comfort_count -= 1
                                        $ mirror_n_cruel_count += 1
                                        if trait_cold:
                                            voice "audio/voices/mirror/intro/cold/9.flac"
                                            cold "I would have kept them in the dark, if I were you.\n"
                                        voice "audio/voices/mirror/intro/hero/12a.flac"
                                        hero "What is that supposed to mean? Whatever awful thing I felt before, it feels so much worse now!\n"
                                        if trait_hunted:
                                            voice "audio/voices/mirror/intro/hunted/6.flac"
                                            hunted "Death. Real death.\n"
                                        if trait_broken:
                                            voice "audio/voices/mirror/intro/broken/6.flac"
                                            broken "This is what we all deserve isn't it?\n"
                                        if trait_stubborn:
                                            voice "audio/voices/mirror/intro/stubborn/6.flac"
                                            stubborn "Screw that! This can't be the end! It just can't!\n"
                                        if trait_opportunist:
                                            voice "audio/voices/mirror/intro/opportunist/6a.flac"
                                            opportunist "You'd better watch your back, you can't get rid of me that easy!\n"
                                        if trait_contrarian:
                                            voice "audio/voices/mirror/intro/contrarian/7.flac"
                                            contrarian "He's just messing with us... right?!\n"
                                        if trait_cheated:
                                            voice "audio/voices/mirror/intro/cheated/6.flac"
                                            cheated "So you're the real puppet master here? Can't believe I tried to help you.\n"
                                        if trait_skeptic:
                                            voice "audio/voices/mirror/intro/skeptic/6.flac"
                                            skeptic "No, that can't be right! There has to be something more!\n"
                                        if trait_paranoid:
                                            voice "audio/voices/mirror/intro/paranoid/6.flac"
                                            paranoid "Can't even trust ourself.\n"
                                        if trait_smitten:
                                            voice "audio/voices/mirror/intro/smitten/6.flac"
                                            smitten "Do it, then. End us all before I die of a broken heart.\n"
                                        jump mirror_n_menu

                                "{i}• I'll see you on the other side. It's going to be okay.{/i}":
                                    jump mirror_n_comfort_join

                                "{i}• [[Approach the mirror.]{/i}":
                                    $ mirror_n_silence_flag = True
                                    jump mirror_approach_join

                            jump mirror_n_menu

                "{i}• [[Approach the mirror.]{/i}":
                    if mirror_hero_scared_flag == False:
                        $ mirror_hero_scared_flag = True
                    jump mirror_approach_join

label mirror_sort_archipelago:

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
