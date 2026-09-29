import Item
import Region

SECONDARY_REGIONS = {
    Region.one,
    Region.one_blade,
    Region.tower_blade,
    Region.spectre_blade,
    Region.nightmare_blade,
    Region.razor,
    Region.razor_blade,
    Region.beast_blade,
    Region.witch_blade,
    Region.prisoner_blade,
    Region.damsel_blade,
}

RESET_REGIONS = {
    Region.adversary_blade,
    Region.tower,
    Region.spectre,
    Region.nightmare,
    Region.beast,
    Region.witch,
    Region.stranger_blade,
    Region.prisoner,
    Region.damsel,
    Region.needle,
    Region.fury,
    Region.apotheosis,
    Region.dragon,
    Region.wraith,
    Region.clarity_blade,
    Region.den,
    Region.wild,
    Region.thorn,
    Region.cage,
    Region.grey,
    Region.happily,
    Region.razor_chap4,
}

NEW_WORLD_REGIONS = {
    Region.stranger_blade,
    Region.damsel,
    Region.needle_hunted_blade,
    Region.fury_weathered_heart,
    Region.apotheosis,
    Region.dragon_kind,
    Region.wraith,
    Region.den_blade,
    Region.wild_blade,
    Region.thorn_blade,
    Region.cage_new_world,
    Region.grey,
    Region.happily_blade,
    Region.razor_chap4,
}

OBLIVION_REGIONS = {
    Region.adversary,
    Region.tower,
    Region.spectre,
    Region.nightmare,
    Region.beast,
    Region.witch,
    Region.prisoner,
    Region.damsel,
    Region.needle,
    Region.fury,
    Region.wraith,
    Region.clarity,
    Region.den,
    Region.thorn,
    Region.cage,
    Region.grey,
}

EVENT_LOCATIONS = SECONDARY_REGIONS | RESET_REGIONS | NEW_WORLD_REGIONS | OBLIVION_REGIONS

REGION_REQUIREMENT = {x: [] for x in RESET_REGIONS | NEW_WORLD_REGIONS | OBLIVION_REGIONS}

REGION_TO_ENTRANCES = {
    Region.needle: {
        Region.needle_hunted,
        Region.needle_skeptic,
    },

    Region.fury: {
        Region.fury_cold,
        Region.fury_contrarian,
        Region.fury_broken,
        Region.fury_tower,
    },

    Region.apotheosis: {
        Region.apotheosis_contrarian,
        Region.apotheosis_paranoid,
    },

    Region.dragon: {
        Region.dragon_kind,
        Region.dragon_harsh,
    },

    Region.wraith: {
        Region.wraith_cheated,
        Region.wraith_paranoid,
        Region.wraith_cold,
        Region.wraith_opportunist,
    },

    Region.den: {
        Region.den_skeptic,
        Region.den_stubborn,
    },

    Region.wild: {
        Region.wild_beast_broken,
        Region.wild_beast_contrarian,
        Region.wild_beast_opportunist,
        Region.wild_beast_stubborn,
        Region.wild_witch_stubborn,
        Region.wild_witch_cheated,
        Region.wild_witch_paranoid,
    },

    Region.thorn: {
        Region.thorn_smitten,
        Region.thorn_cheated,
    },

    Region.cage: {
        Region.cage_paranoid,
        Region.cage_cheated,
        Region.cage_broken,
    },

    Region.grey: {
        Region.grey_drowned,
        Region.grey_burned,
    },

    Region.happily: {
        Region.happily_skeptic,
        Region.happily_opportunist,
    },

    Region.razor_chap4: {
        Region.razor_no_way_broken,
        Region.razor_no_way_paranoid,
        Region.razor_race_broken,
        Region.razor_race_paranoid,
        Region.razor_race_stubborn,
    },

    Region.fury_weathered_heart: {
        Region.fury_cold,
        Region.fury_contrarian,
        Region.fury_broken,
        Region.fury_tower_blade,
    },

    Region.cage_new_world: {
        Region.cage_paranoid_blade,
        Region.cage_cheated,
        Region.cage_broken,
    },

    #Specials Region
    Region.fury_broken_cold: {
        Region.fury_broken,
        Region.fury_cold,
    },

    Region.fury_unwound_heart: {
        Region.fury_contrarian,
        Region.fury_tower,
    },

    Region.cage_not_paranoid: {
        Region.cage_cheated,
        Region.cage_broken,
    },
}

RANDO_ENTRANCE = {
    Region.adversary: Region.adversary,
    Region.tower: Region.tower,
    Region.spectre: Region.spectre,
    Region.nightmare: Region.nightmare,
    Region.razor: Region.razor,
    Region.beast: Region.beast,
    Region.witch: Region.witch,
    Region.stranger: Region.stranger,
    Region.prisoner: Region.prisoner,
    Region.damsel: Region.damsel,

    Region.needle_hunted: Region.needle_hunted,
    Region.needle_skeptic: Region.needle_skeptic,

    Region.fury_broken: Region.fury_broken,
    Region.fury_cold: Region.fury_cold,
    Region.fury_contrarian: Region.fury_contrarian,

    Region.fury_tower: Region.fury_tower,

    Region.apotheosis_contrarian: Region.apotheosis_contrarian,
    Region.apotheosis_paranoid: Region.apotheosis_paranoid,

    Region.dragon_kind: Region.dragon_kind,
    Region.dragon_harsh: Region.dragon_harsh,

    Region.wraith_cheated: Region.wraith_cheated,
    Region.wraith_paranoid: Region.wraith_paranoid,

    Region.clarity: Region.clarity,

    Region.wraith_cold: Region.wraith_cold,
    Region.wraith_opportunist: Region.wraith_opportunist,

    Region.razor_no_way_broken: Region.razor_no_way_broken,
    Region.razor_no_way_paranoid: Region.razor_no_way_paranoid,

    Region.razor_race_broken: Region.razor_race_broken,
    Region.razor_race_paranoid: Region.razor_race_paranoid,
    Region.razor_race_stubborn: Region.razor_race_stubborn,

    Region.den_skeptic: Region.den_skeptic,
    Region.den_stubborn: Region.den_stubborn,

    Region.wild_beast_broken: Region.wild_beast_broken,
    Region.wild_beast_contrarian: Region.wild_beast_contrarian,
    Region.wild_beast_opportunist: Region.wild_beast_opportunist,
    Region.wild_beast_stubborn: Region.wild_beast_stubborn,

    Region.thorn_smitten: Region.thorn_smitten,
    Region.thorn_cheated: Region.thorn_cheated,

    Region.wild_witch_stubborn: Region.wild_witch_stubborn,
    Region.wild_witch_cheated: Region.wild_witch_cheated,
    Region.wild_witch_paranoid: Region.wild_witch_paranoid,

    Region.cage_paranoid: Region.cage_paranoid,
    Region.cage_cheated: Region.cage_cheated,
    Region.cage_broken: Region.cage_broken,

    Region.grey_drowned: Region.grey_drowned,

    Region.happily_skeptic: Region.happily_skeptic,
    Region.happily_opportunist: Region.happily_opportunist,

    Region.grey_burned: Region.grey_burned,
}

ENTRANCE_REQUIREMENT = {
    # Chap 2
    Region.adversary: Region.one_blade,
    Region.tower: Region.one_blade,
    Region.spectre: Region.one_blade,
    Region.nightmare: Region.one,
    Region.razor: Region.one_blade,
    Region.beast: Region.one_blade,
    Region.witch: Region.one_blade,
    Region.stranger: Region.one,
    Region.prisoner: Region.one_blade,
    Region.damsel: Region.one,

    # Adversary
    Region.needle_hunted: Region.adversary_blade,
    Region.needle_skeptic: Region.adversary_blade,

    Region.fury_broken: Region.adversary,
    Region.fury_cold: Region.adversary,
    Region.fury_contrarian: Region.adversary,

    # Tower
    Region.fury_tower: Region.tower_blade,

    Region.apotheosis_contrarian: Region.tower_blade,
    Region.apotheosis_paranoid: Region.tower,

    # Spectre
    Region.dragon_kind: Region.spectre_blade,
    Region.dragon_harsh: Region.spectre_blade,

    Region.wraith_cheated: Region.spectre,
    Region.wraith_paranoid: Region.spectre,

    # Nightmare
    Region.clarity: Region.nightmare,

    Region.wraith_cold: Region.nightmare_blade,
    Region.wraith_opportunist: Region.nightmare_blade,

    # Razor
    Region.razor_no_way_broken: Region.razor,
    Region.razor_no_way_paranoid: Region.razor,

    Region.razor_race_broken: Region.razor_blade,
    Region.razor_race_paranoid: Region.razor_blade,
    Region.razor_race_stubborn: Region.razor_blade,

    # Beast
    Region.den_skeptic: Region.beast,
    Region.den_stubborn: Region.beast_blade,

    Region.wild_beast_broken: Region.beast,
    Region.wild_beast_contrarian: Region.beast,
    Region.wild_beast_opportunist: Region.beast_blade,
    Region.wild_beast_stubborn: Region.beast_blade,

    # Witch
    Region.thorn_smitten: Region.witch_blade,
    Region.thorn_cheated: Region.witch_blade,

    Region.wild_witch_stubborn: Region.witch_blade,
    Region.wild_witch_cheated: Region.witch_blade,
    Region.wild_witch_paranoid: Region.witch,

    # Prisoner
    Region.cage_paranoid: Region.prisoner_blade,
    Region.cage_cheated: Region.prisoner,
    Region.cage_broken: Region.prisoner,

    Region.grey_drowned: Region.prisoner_blade,

    # Damsel
    Region.happily_skeptic: Region.damsel,
    Region.happily_opportunist: Region.damsel,

    Region.grey_burned: Region.damsel_blade,
}

def get_bladeless_name(region):
    return region.removesuffix(" [Blade Only]").removesuffix(" [Sword Only]")

def get_main_region_name(region):
    return get_bladeless_name(region.split(" (", 1)[0])

def get_blade_name_for_region(region):
    if " - " in region:
        region = region.split(" - ", 1)[1]
    return "Pristine Blade - " + get_main_region_name(region)

def fill_region_tokens():
    for region_name, dict_requirements in REGION_REQUIREMENT.items():
        if "Chapter II - " not in region_name:
            new_entrance = RANDO_ENTRANCE.get(get_bladeless_name(region_name))
            if new_entrance is not None:
                dict_requirements = [[ENTRANCE_REQUIREMENT[new_entrance], None]]
            else:
                all_entrance = REGION_TO_ENTRANCES[get_bladeless_name(region_name)]
                for entrance in all_entrance:
                    blade = None
                    if entrance != get_bladeless_name(entrance):
                        blade = get_blade_name_for_region(entrance)
                    dict_requirements.append([ENTRANCE_REQUIREMENT[RANDO_ENTRANCE[get_bladeless_name(entrance)]], blade])

fill_region_tokens() #DEBUG Devra attendre connexion server + entrance rando info avant de se faire

def max_reset(archipelago, regions: set[str], want: int, skip_minus_one: bool = False) -> bool:
    max_count = (archipelago.count_item(Item.invitation) + int(skip_minus_one)) if archipelago.get_gift_rando in [1, 3] else 5
    if max_count < want and regions != OBLIVION_REGIONS:
        return False

    accessible_region = {region for region in EVENT_LOCATIONS if archipelago.can_access_region(region)}

    chap2_regions = set()
    chap3_regions = set()
    for r in regions:
        if "Chapter II -" in r:
            chap2_regions.add(r)
        else:
            chap3_regions.add(r)

    usable_chap2 = {get_bladeless_name(r) for r in chap2_regions if r in accessible_region}
    if len(usable_chap2) >= want:
        return True

    usable_chap3 = 0
    used_chapter = set(usable_chap2)
    candidates = []
    for r in chap3_regions:
        if r in accessible_region:
            available_region = []
            for e in REGION_REQUIREMENT[r]:
                if e[0] in accessible_region and get_bladeless_name(e[0]) not in used_chapter:
                    import renpy
                    if e[1] is None or renpy.store.hasThisBlade(e[1]):
                        available_region.append(e[0])
            
            if available_region:
                candidates.append((r, available_region))
    candidates.sort(key=lambda x: len(x[1]))

    for r, region_entrance in candidates:
        available_region = []
        for entrance in region_entrance:
            bladeless_entrance = get_bladeless_name(entrance)
            if bladeless_entrance not in used_chapter:
                available_region.append(bladeless_entrance)

        if available_region: #faire en sorte que cela couvre bien toute les possibilité (si un seul on le prend, si plusieurs il faut vérifier tous les cas)
            used_chapter.add(get_bladeless_name(r))
            used_chapter.add(available_region[0])
            usable_chap3 += 1
            if len(usable_chap2) + usable_chap3 >= want:
                return True

    return False


def max_reachable_vessels(archipelago, want: int, entity: bool = True, skip_minus_one: bool = False) -> bool:
    result = archipelago.can_access_function("max_reachable", want)
    if result:
        return True

    has_princess = archipelago.get_chapter_access() in [0, 2] or archipelago.has_item(Item.goddess)
    if not entity and want == 1:
        result = max_reset(archipelago, RESET_REGIONS, want, skip_minus_one)
    elif entity and want == 5:
        has_narrator = not archipelago.get_narrator_rando() or archipelago.has_item(Item.narrator)
        result = max_reset(archipelago, RESET_REGIONS, want, skip_minus_one) and has_princess and has_narrator
    else:
        result = max_reset(archipelago, RESET_REGIONS, want, skip_minus_one) and has_princess

    if result:
        archipelago.inform_access_function("max_reachable", want - int(skip_minus_one or not entity))
    return result


def can_reach_new_world(archipelago) -> bool:
    result = archipelago.can_access_function("new_world", 5)
    if result:
        return True

    has_princess = archipelago.get_chapter_access() in [0, 2] or archipelago.has_item(Item.goddess)
    has_narrator = not archipelago.get_narrator_rando() or archipelago.has_item(Item.narrator)

    result = False
    if has_princess and has_narrator:
        result = max_reset(archipelago, NEW_WORLD_REGIONS, 5)

    if result:
        archipelago.inform_access_function("new_world", 5)
    return result


def can_reach_oblivion(archipelago, want: int) -> bool:
    result = archipelago.can_access_function("oblivion", want)
    if result:
        return True

    result = max_reset(archipelago, OBLIVION_REGIONS, want)

    if result:
        archipelago.inform_access_function("oblivion", want)
    return result


def gallery_checker(archipelago, name: str):
    from GALLERY_REQUIREMENTS import GALLERY_REQUIREMENTS
    region, function, *args = GALLERY_REQUIREMENTS[name]

    region_access = archipelago.can_access_region(region)
    function_access = True

    if function is not None and region_access:
        function_access = function(archipelago, *args)
    
    return region_access and function_access