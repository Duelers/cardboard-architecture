import typing

import card_types
import factions
import base
import abilities as _abilities
import effects as _effects


class CardModel(base.BaseModel):
    name: str
    cost: int
    faction: factions.Faction = factions.neutral


class MinionCard(CardModel):
    type: typing.Literal[card_types.minion] = card_types.minion
    attack: int
    max_health: int
    tribes: typing.List[str] = []
    abilities: typing.Union[
        _abilities.Ability,
        typing.List[_abilities.Ability]
    ]


class SpellCard(CardModel):
    type: typing.Literal[card_types.spell] = card_types.spell
    effects: typing.Union[
        _effects.Effect,
        typing.List[_effects.Effect]
    ]


class ArtifactCard(CardModel):
    type: typing.Literal[card_types.artifact] = card_types.artifact
    abilities: typing.Union[
        _abilities.Ability,
        typing.List[_abilities.Ability]
    ]


Card = typing.Union[SpellCard, MinionCard, ArtifactCard]


class CardRoot(base.BaseModel):
    __root__: typing.Union[Card]
