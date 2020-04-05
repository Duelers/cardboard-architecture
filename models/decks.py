import pydantic
import typing

import models.cards

class MasterDeck(pydantic.BaseModel):
    general_id: str
    cards: typing.List[models.cards.CardInclusionInDeck]


class CurrentDeck(pydantic.BaseModel):
    cards: typing.List[models.cards.CASTABLE]
