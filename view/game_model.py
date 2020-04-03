import models
from . import presentation


class Model:
    def __init__(self):
        self._game_state: models.GameState = models.GameState.new_game()

    def update(self, update: models.GameUpdate):
        self._game_state = update.game_state
        presentation.update(update)
