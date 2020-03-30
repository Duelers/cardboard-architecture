import models
import models.game_update
from . import video


class Presentation:
    def __init__(self):
        self.video = video

    def present(self, update: models.game_update.GameUpdate):
        self.video.display_board(update.game_state)

        if update.event:
            self.video.play_animation(update.event)


_presentation = Presentation()


def update(update: models.game_update.GameUpdate):
    _presentation.present(update)
