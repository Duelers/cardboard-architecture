import pydantic
import typing

MAX_CARDS_PER_DECK = 3


class CardInclusionInDeck(pydantic.BaseModel):
    card_id: str
    count: pydantic.conint(ge=0, le=MAX_CARDS_PER_DECK)


class Card(pydantic.BaseModel):
    name: str


class Castable(Card):
    cost: pydantic.conint(ge=0)


class Unit(Card):
    attack: pydantic.conint(ge=0)
    max_health: pydantic.conint(ge=0)

    current_health: typing.Optional[int] = None
    # Can technically be negative at times. Relevant when taking damage and then healing in response.
    # None while off the board. Set to max_health when etb.


class General(Unit):
    type: typing.Literal['general'] = 'general'


class Minion(Unit, Castable):
    type: typing.Literal['minion'] = 'minion'


CASTABLE = typing.Union[Minion]
CARD = typing.Union[General, Minion]  # Todo see if I can remove duplication with card_parsing
