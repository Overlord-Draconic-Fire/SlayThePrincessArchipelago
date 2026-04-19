"""
Blade to chapter mapping for Slay the Princess Archipelago randomizer.
Maps blade item values to their corresponding chapters.
Used by hasThisBlade() to check blade possession with fallback hierarchy.
"""

import Item

# Mapping of blade item values to chapter numbers
BLADE_CHAPTER_MAP = {
    # Chapter 1
    Item.blade_princess: 1,
    
    # Chapter 2
    Item.blade_adversary: 2,
    Item.blade_tower: 2,
    Item.blade_spectre: 2,
    Item.blade_nightmare: 2,
    Item.blade_razor: 2,
    Item.blade_beast: 2,
    Item.blade_witch: 2,
    Item.blade_stranger: 2,
    Item.blade_prisoner: 2,
    Item.blade_damsel: 2,
    
    # Chapter 3
    Item.blade_needle: 3,
    Item.blade_fury: 3,
    Item.blade_apotheosis: 3,
    Item.blade_dragon: 3,
    Item.blade_clarity: 3,
    Item.blade_den: 3,
    Item.blade_wild: 3,
    Item.blade_thorn: 3,
    Item.blade_cage: 3,
    Item.blade_grey: 3,
    Item.blade_happily: 3,
    
    # End
    Item.blade_goddess: 4,
}
