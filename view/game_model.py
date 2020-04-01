import models
from . import presentation


class Model:
    def __init__(self):
        self._game_state: models.GameState = None

    def update(self, update: models.GameUpdate):
        self._game_state = update.game_state
        presentation.update(update)
