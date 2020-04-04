import typing

lyonar = "lyonar"
songhai = "songhai"
vetruvian = "vetruvian"
abyssian = "abyssian"
magmar = "magmar"
vanar = "vanar"
neutral = "neutral"

Faction = typing.Union[
    typing.Literal[lyonar],
    typing.Literal[songhai],
    typing.Literal[vetruvian],
    typing.Literal[abyssian],
    typing.Literal[magmar],
    typing.Literal[vanar],
    typing.Literal[neutral],
]
