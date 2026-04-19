def _gallery_list(route_name, count) -> list[str]:
    # Index 0 is intentionally empty so callers can use 1-based gallery indexes.
    return [""] + [f"{route_name} (Gallery {i})" for i in range(1, count + 1)]

# Beginnings & Endings
princess: list[str] = _gallery_list("The Hero and the Princess", 18)
spaceBetween: list[str] = _gallery_list("The Spaces Between", 9)
finale: list[str] = _gallery_list("The End of Everything", 20)

# 1st Row
adversary: list[str] = _gallery_list("The Adversary", 20)
tower: list[str] = _gallery_list("The Tower", 13)
spectre: list[str] = _gallery_list("The Spectre", 18)
nightmare: list[str] = _gallery_list("The Nightmare", 19)
razor: list[str] = _gallery_list("The Razor", 20)
beast: list[str] = _gallery_list("The Beast", 17)
witch: list[str] = _gallery_list("The Witch", 20)
stranger: list[str] = _gallery_list("The Stranger", 12)
prisoner: list[str] = _gallery_list("The Prisoner", 17)
damsel: list[str] = _gallery_list("The Damsel", 20)

# 2nd Row
needle: list[str] = _gallery_list("The Eye of the Needle", 20)
fury: list[str] = _gallery_list("The Fury", 20)
apotheosis: list[str] = _gallery_list("The Apotheosis", 20)
dragon: list[str] = _gallery_list("The Princess and the Dragon", 20)
wraith: list[str] = _gallery_list("The Wraith", 11)
clarity: list[str] = _gallery_list("The Moment of Clarity", 14)
den: list[str] = _gallery_list("The Den", 20)
wild: list[str] = _gallery_list("The Wild", 12)
thorn: list[str] = _gallery_list("The Thorn", 19)
cage: list[str] = _gallery_list("The Cage", 20)
grey: list[str] = _gallery_list("The Grey", 20)
happy: list[str] = _gallery_list("Happily Ever After", 20)
