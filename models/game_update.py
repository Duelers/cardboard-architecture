import typing

import pydantic

import models.events


class GameUpdate(pydantic.BaseModel):
    game_state: models.GameState
    event: typing.Optional[models.events.BaseEvent]
