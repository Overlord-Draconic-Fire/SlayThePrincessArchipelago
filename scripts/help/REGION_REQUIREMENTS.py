"""
Region access requirements for Slay the Princess Archipelago randomizer.
Maps region names to required items (princesses and voices).
"""

import Item
import Region

# Mapping of region names to required items [princess, voice(s)]
REGION_REQUIREMENTS = {
    # Chapter II regions - princess + corresponding voice
    Region.adversary: [Item.adversary, Item.stubborn],
    Region.tower: [Item.tower, Item.broken],
    Region.spectre: [Item.spectre, Item.cold],
    Region.nightmare: [Item.nightmare, Item.paranoid],
    Region.razor: [Item.razor, Item.cheated],
    Region.beast: [Item.beast, Item.hunted],
    Region.witch: [Item.witch, Item.opportunist],
    Region.stranger: [Item.stranger, Item.contrarian],
    Region.prisoner: [Item.prisoner, Item.skeptic],
    Region.damsel: [Item.damsel, Item.smitten],
    
    # Chapter III - Eye of the Needle (from Adversary → Stubborn)
    Region.needle_hunted: [Item.needle, Item.stubborn, Item.hunted],
    Region.needle_skeptic: [Item.needle, Item.stubborn, Item.skeptic],
    
    # Chapter III - Fury (from Adversary → Stubborn)
    Region.fury_cold: [Item.fury, Item.stubborn, Item.cold],
    Region.fury_contrarian: [Item.fury, Item.stubborn, Item.contrarian],
    Region.fury_broken: [Item.fury, Item.stubborn, Item.broken],
    Region.fury_tower: [Item.fury, Item.broken, Item.stubborn],  # From Tower → Broken
    
    # Chapter III - Apotheosis (from Tower → Broken)
    Region.apotheosis_contrarian: [Item.apotheosis, Item.broken, Item.contrarian],
    Region.apotheosis_paranoid: [Item.apotheosis, Item.broken, Item.paranoid],
    
    # Chapter III - Dragon (from Spectre → Cold)
    Region.dragon_kind: [Item.dragon, Item.cold, Item.opportunist],
    Region.dragon_harsh: [Item.dragon, Item.cold, Item.opportunist],
    
    # Chapter III - Wraith (cheated/paranoid from Spectre → Cold, cold/opportunist from Nightmare → Paranoid)
    Region.wraith_cheated: [Item.wraith, Item.cold, Item.cheated],
    Region.wraith_paranoid: [Item.wraith, Item.cold, Item.paranoid],
    Region.wraith_cold: [Item.wraith, Item.paranoid, Item.cold],
    Region.wraith_opportunist: [Item.wraith, Item.paranoid, Item.opportunist],
    
    # Chapter III - Clarity (needs all voices)
    Region.clarity: [Item.clarity, Item.stubborn, Item.broken, Item.cold, Item.paranoid, Item.cheated, Item.hunted, Item.opportunist, Item.contrarian, Item.skeptic, Item.smitten],
    
    # Chapter III and IV - Razor variants (from Razor → Cheated)
    Region.razor_chap3: [Item.razor, Item.stubborn, Item.broken, Item.cold, Item.paranoid, Item.cheated, Item.hunted, Item.opportunist, Item.contrarian, Item.skeptic, Item.smitten],

    # No use for these
    Region.razor_no_way_broken: [Item.razor, Item.cheated, Item.contrarian, Item.broken],
    Region.razor_no_way_paranoid: [Item.razor, Item.cheated, Item.contrarian, Item.paranoid],
    Region.razor_no_way_stubborn: [Item.razor, Item.cheated, Item.contrarian, Item.stubborn],
    Region.razor_race_broken: [Item.razor, Item.cheated, Item.hunted, Item.broken],
    Region.razor_race_paranoid: [Item.razor, Item.cheated, Item.hunted, Item.paranoid],
    Region.razor_race_stubborn: [Item.razor, Item.cheated, Item.hunted, Item.stubborn],
    
    # Chapter III - Den (from Beast → Hunted)
    Region.den_skeptic: [Item.den, Item.hunted, Item.skeptic],
    Region.den_stubborn: [Item.den, Item.hunted, Item.stubborn],
    
    # Chapter III - Wild (all voices)
    Region.wild_beast_broken: [Item.wild, Item.hunted, Item.broken],
    Region.wild_beast_contrarian: [Item.wild, Item.hunted, Item.contrarian],
    Region.wild_beast_opportunist: [Item.wild, Item.hunted, Item.opportunist],
    Region.wild_beast_stubborn: [Item.wild, Item.hunted, Item.stubborn],
    Region.wild_witch_stubborn: [Item.wild, Item.opportunist, Item.stubborn],
    Region.wild_witch_cheated: [Item.wild, Item.opportunist, Item.cheated],
    Region.wild_witch_paranoid: [Item.wild, Item.opportunist, Item.paranoid],
    
    # Chapter III - Thorn (from Witch → Opportunist)
    Region.thorn_smitten: [Item.thorn, Item.opportunist, Item.smitten],
    Region.thorn_cheated: [Item.thorn, Item.opportunist, Item.cheated],
    
    # Chapter III - Cage (from Prisoner → Skeptic)
    Region.cage_paranoid: [Item.cage, Item.skeptic, Item.paranoid],
    Region.cage_cheated: [Item.cage, Item.skeptic, Item.cheated],
    Region.cage_broken: [Item.cage, Item.skeptic, Item.broken],
    
    # Chapter III - Grey (from Prisoner → Skeptic and Damsel → Smitten)
    Region.grey_drowned: [Item.grey, Item.skeptic, Item.cold],
    Region.grey_burned: [Item.grey, Item.smitten, Item.cold],
    
    # Epilogue - Happily Ever After (from Damsel → Smitten)
    Region.happily_skeptic: [Item.happily, Item.skeptic],
    Region.happily_opportunist: [Item.happily, Item.opportunist],

    # The Long Quiet - The Shifting Mound
    Region.goddess: [Item.goddess],
}
