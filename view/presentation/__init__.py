import models
from . import video


class Presentation:
    def __init__(self):
        self.video = video

    def update(self, update: models.GameUpdate):
        if update.effect:
            self.video.play_animation(update.effect, update.game_state)
        self.draw_game_state(update.game_state)

    def draw_game_state(self, game_state: models.GameState):
        self.video.display_board(game_state)
        self.video.display_deck(game_state)