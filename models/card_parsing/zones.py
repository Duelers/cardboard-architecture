import typing

in_play = "in_play"
hand = "hand"
graveyard = "graveyard"

CardZone = typing.Union[typing.Literal[hand],
                        typing.Literal[graveyard]]

Zone = typing.Union[
    typing.Literal[in_play],
    CardZone
]
