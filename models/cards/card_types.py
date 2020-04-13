import typing

minion = "minion"
artifact = "artifact"
spell = "spell"
general = "general"
# unit = "unit" #includes minions and generals

CardType = typing.Union[
    typing.Literal[minion],
    typing.Literal[artifact],
    typing.Literal[spell],
    typing.Literal[general]
]
