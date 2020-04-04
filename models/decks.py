import pydantic
import typing

import models.cards

class Deck(pydantic.BaseModel):
    general: models.cards.General
    cards: typing.List[models.cards.CARD]