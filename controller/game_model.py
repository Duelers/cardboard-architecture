import typing
import models
from . import networking_to_view


class Model:
    def __init__(self):
        self._game_state: models.GameState = models.GameState.new_game()
        self._effect_log: typing.List[models.BaseEffect] = []

    @property
    def game_state(self):
        return self._game_state

    def update(self, update: models.GameUpdate) -> typing.NoReturn:
        self._game_state = update.game_state

        if update.effect:
            self._effect_log.append(update.effect)

        networking_to_view.send_update(update)
