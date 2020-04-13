import typing

you = "you"
opponent = "opponent"

Player = typing.Union[
    typing.Literal[you],
    typing.Literal[opponent]
]
