import typing

import models
from .presentation import Presentation
import pprint


class Model:
    def __init__(self, presentation: Presentation):
        self._game_state: typing.Optional[models.GameState] = None
        self.presentation = presentation

    def initialize(self, game_state: models.GameState):
        self._game_state = game_state

    def update(self, update: models.GameUpdate):
        if not self._game_state:
            raise ValueError('Game has not yet been initialized.')
        self._game_state = update.game_state
        self.presentation.update(update)

    def present(self):
        """This is here for when you want to draw without updating, such as at the beginning of the game.
        Might be removable.
        """
        self.presentation.draw_game_state(self._game_state)

    def display_options(self, options):
        options = [(i, option) for i, option in enumerate(options)]
        pprint.pp(options)
