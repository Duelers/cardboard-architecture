"""This is mostly a wrapper for card_models.cards"""
import pydantic
import typing

import models.cells
from .. import players

from . import cards, base, factions, locations, card_types, abilities as _abilities, effects as _effects

MAX_CARDS_PER_DECK = 3


class CardInclusionInDeck(pydantic.BaseModel):
    card_id: str
    count: pydantic.conint(ge=0, le=MAX_CARDS_PER_DECK)


class BaseCard(base.BaseModel):
    name: str
    faction: factions.Faction = factions.neutral


class PermanentMixin(pydantic.BaseModel):
    """Mixin for cards that stay on the field"""
    abilities: typing.List[_abilities.Ability] = []


class CastableMixin(pydantic.BaseModel):
    """Mixin for cards that can be cast"""
    cost: pydantic.conint(ge=0)


class UnitCard(BaseCard, PermanentMixin):
    attack: pydantic.conint(ge=0)
    max_health: pydantic.conint(ge=0)

    # move_options: locations.MultipleLocation = locations.LocationFromCoords(row=0, col=0)
    move_options: base.MultipleGetter = locations.LocationFromCoords(row=0, col=0)


class GeneralCard(UnitCard):
    pass


class MinionCard(UnitCard, CastableMixin):
    tribes: typing.List[str] = []


class SpellCard(BaseCard, CastableMixin):
    effects: typing.List[_effects.Effect]


class ArtifactCard(BaseCard, CastableMixin, PermanentMixin):
    pass


class InGameCardMixin(pydantic.BaseModel):
    instance_id: typing.Optional[int] = None  # Used to keep cards unique in the gamestate.
    player: players.PlayerNumber = None  # should just be on permanents.


class InGameUnit(UnitCard, InGameCardMixin):
    current_health: typing.Optional[int] = None
    # Can technically be negative at times. Relevant when taking damage and then healing in response.
    # None while off the board. Set to max_health when etb.


class General(GeneralCard, InGameUnit):
    pass


class Minion(MinionCard, InGameUnit):
    pass
