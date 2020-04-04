import typing

your_general = "your_general"
opponent_general = "opponent_general"

Generals = typing.Union[
    typing.Literal[your_general],
    typing.Literal[opponent_general]
]
