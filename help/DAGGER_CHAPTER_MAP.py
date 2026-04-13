"""
Dagger to chapter mapping for Slay the Princess Archipelago randomizer.
Maps dagger item values to their corresponding chapters.
Used by hasThisDagger() to check dagger possession with fallback hierarchy.
"""

import Item

# Mapping of dagger item values to chapter numbers
DAGGER_CHAPTER_MAP = {
    # Chapter 1
    Item.dagger_princess: 1,
    
    # Chapter 2
    Item.dagger_adversary: 2,
    Item.dagger_tower: 2,
    Item.dagger_spectre: 2,
    Item.dagger_nightmare: 2,
    Item.dagger_razor: 2,
    Item.dagger_beast: 2,
    Item.dagger_witch: 2,
    Item.dagger_stranger: 2,
    Item.dagger_prisoner: 2,
    Item.dagger_damsel: 2,
    
    # Chapter 3
    Item.dagger_needle: 3,
    Item.dagger_fury: 3,
    Item.dagger_apotheosis: 3,
    Item.dagger_dragon: 3,
    Item.dagger_den: 3,
    Item.dagger_wild: 3,
    Item.dagger_thorn: 3,
    Item.dagger_cage: 3,
    Item.dagger_grey: 3,
    Item.dagger_happily: 3,
    
    # End
    Item.dagger_goddess: 4,
}
