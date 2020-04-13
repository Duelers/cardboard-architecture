import abc

import pydantic
import typing

import models.cards


class MasterDeck(pydantic.BaseModel):
    """A decklist out of game. Contains everything needed for gamestate to construct a CurrentDeck."""
    general_id: str
    cards: typing.List[models.cards.CardInclusionInDeck]


class CardArea(pydantic.BaseModel, abc.ABC):  # todo rename? It's any collection of cards.

    def remove(self, card: models.cards.CastableMixin):
        raise NotADirectoryError


class CurrentDeck(CardArea):
    cards: typing.List[models.cards.CastableMixin]

    def remove(self, card: models.cards.CastableMixin):
        self.cards.remove(card)
