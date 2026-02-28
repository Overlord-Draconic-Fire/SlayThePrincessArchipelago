label variable_staging:

    default default_mouse = "default"
    default pacifism_count = 0
    default fury_pacifism = False
    # what ending did you get; options are — "liberation" (leave with the awakened mound); "oblivion" (destroy enough timelines that the mound can never be finished); "slay" (slay the princess); "good" (the good ending — first run only!); "slay_whoops" (slay, but the voices are mad at you); "loop" (reset the loop); "leave" (leave together)

    default final_ending = ""

    # current run stuff

    default current_run_mirror_comment = False
    default current_run_mirror_touched = False

    default basement_1_talked = False

    # what chapter is the player on?
    default current_loop = 1

    # how many "meta" loops has the player finished
    default loops_finished = 0

    # how many loops have been destroyed through flight
    default loops_destroyed = 0

    # is the player locked out of the void ending?

    default void_locked = False

    # is the knife backwards
    default knife_backwards = False

    # defining the order of princesses the player has encountered
    default first_mound = ""
    default second_mound = ""
    default third_mound = ""
    default fourth_mound = ""
    default fifth_mound = ""

    # booleans marking if a given princess has been encountered

    default adversary_encountered = False
    default beast_encountered = False
    default damsel_encountered = False
    default nightmare_encountered = False
    default prisoner_encountered = False
    default razor_encountered = False
    default spectre_encountered = False
    default stranger_encountered = False
    default tower_encountered = False
    default witch_encountered = False

    default needle_encountered = False
    default den_encountered = False
    default clarity_encountered = False
    default thorn_encountered = False
    default apotheosis_encountered = False

    default wild_encountered = False
    default fury_encountered = False
    default wraith_encountered = False
    default grey_encountered = False

    default cage_encountered = False
    default dragon_encountered = False
    default happy_encountered = False

    # defining relationship variables for meta-princess

    default princess_satisfy = 0
    default princess_deny = 0
    default princess_killed_ending = 0
    default player_killed_ending = 0
    default princess_free = 0
    default princess_kept = 0

    # redoing variables

    # defining what voices have been met

    default stubborn_met = False
    default hunted_met = False
    default smitten_met = False
    default paranoid_met = False
    default skeptic_met = False
    default cheated_met = False
    default cold_met = False
    default contrarian_met = False
    default broken_met = False
    default opportunist_met = False

    # defining what princesses have been 'fed' to the mound

    default adversary_fed = False
    default needle_fed = False
    default beast_fed = False
    default den_fed = False
    default damsel_fed = False
    default nightmare_fed = False
    default clarity_fed = False
    default prisoner_fed = False
    default razor_fed = False
    default spectre_fed = False
    default stranger_fed = False
    default tower_fed = False
    default apotheosis_fed = False
    default witch_fed = False
    default thorn_fed = False
    default wraith_fed = False
    default wild_fed = False
    default grey_fed = False
    default fury_fed = False

    # defining strings to hold which "ending" was achieved on a given route, as it relates to the final encounter with the mound(so fury endings are sources rather than endings etc); values are not stored for chapter 2 endings which flow into a chapter 3 — these variables only store what worldstate is gifted to the mound

    # possible values: pacifism; tower; unarmed.
    default fury_end = ""

    # possible values: drown; burn
    default grey_end = ""

    # possible values: joined; separate; slay
    default wild_end = ""

    # possible values: slay; free
    default wraith_end = ""

    # possible values: infinite
    default adversary_end = ""

    # possible values: fight_fail; flee_fail; fight_succeed; free
    default adversary_2_end = ""

    # possible values: free
    default beast_end = ""

    # possible values: fight_fail; fight_succeed; free_fail; free_succeed
    default beast_2_end = ""

    # possible values: unreal; free
    default damsel_end = ""

    # possible values: free
    default nightmare_end = ""

    # possible values: free
    default nightmare_2_end = ""

    # possible values: stuck forever; free.
    default prisoner_end = ""

    # possible values: fight; pacifism
    default razor_end = ""

    # possible values: free; slay
    default spectre_end = ""

    # possible values: all
    default stranger_end = ""

    # possible values: free
    default tower_end = ""

    # possible values: submit; fight
    default tower_2_end = ""

    # possible values: witch_betray; player_betray
    default witch_end = ""

    # possible values: free; free_kiss; slay_attempt; stuck; stuck_together
    default thorn_end = ""


    # PRISTINE CUT

    default happy_end = ""
    default dragon_end = ""
    default cage_end = ""

    # defining player death count at hands of princess; princess death count; and mutual death count; current modifier for current metaloop; meta modifier for the mound

    default current_princess_death = 0
    default current_player_death = 0
    default current_mutual_death = 0

    default meta_princess_death = 0
    default meta_player_death = 0
    default meta_mutual_death = 0

    # extra flags for chapter 1

    default nightmare_join_fled = False
    default razor_revival = False
    default tower_unharmed = False

    # a fake variable for menus that do nothing
    default fake_variable = False

    # a fake variable to construct visible false options
    default false_choice = False

return
