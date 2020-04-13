import typing

import pydantic

from . import players

# import card_models.zones todo some duplication here?

Deck = 'deck'
Hand = 'hand'
Graveyard = 'graveyard'

PLAYER_ZONE_NAMES = typing.Union[
    typing.Literal[Deck],
    typing.Literal[Hand],
    typing.Literal[Graveyard]
]


class PlayerZone(pydantic.BaseModel):
    zone: PLAYER_ZONE_NAMES
    player: players.PlayerNumber
