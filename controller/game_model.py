import typing

import models.game_update
from . import networking_to_view

import models.events


class Model:
    model: models.GameState = None
    event_log: typing.List[models.events.BaseEvent] = []

    @classmethod
    def get(cls):
        if cls.model:
            return cls.model.copy(deep=True)

    @classmethod
    def update(cls, update: models.game_update.GameUpdate):
        cls.model = update.game_state

        if update.event:
            cls.event_log.append(update.event)

        networking_to_view.send_update(update)
