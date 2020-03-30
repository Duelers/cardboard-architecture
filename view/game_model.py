import models
import models.game_update
from . import presentation


class Model:
    model: models.GameState = None

    @classmethod
    def update(cls, update: models.game_update.GameUpdate):
        cls.model = update.game_state
        presentation.update(update)
