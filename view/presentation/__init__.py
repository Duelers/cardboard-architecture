import models
from . import video


class Presentation:
    def __init__(self):
        self.video = video

    def present(self, update: models.GameUpdate):
        self.video.display_board(update.game_state)

        if update.event:
            self.video.play_animation(update.event, update.game_state)


_presentation = Presentation()


def update(update: models.GameUpdate):
    _presentation.present(update)
