from __future__ import annotations

import typing

import models.cells
from . import game_model
from . import presentation

if typing.TYPE_CHECKING:
    import controller


class View:
    def __init__(self):
        self.model = game_model.Model(presentation.Presentation())
        self.controller: controller.Controller = None  # Must be set before use.

    def set_controller(self, controller):
        """Must be called before use."""
        self.controller = controller

    def receive_game_state(self, game_state: models.GameState):
        """Updates the view's model of the game."""
        self.model.initialize(game_state)
        self.model.present()

    def receive_update(self, update: models.GameUpdate):
        self.model.update(update)

    def make_choice(self, choices: typing.List):
        choice = -1
        while choice not in range(len(choices)):
            print("Make a selection")
            choice = int(input())

        self.controller.receive_choice(choice)

    def receive_available_actions(self, actions: typing.List[models.BaseAction]):
        self.model.display_options(actions)
        self.make_choice(actions)

    def dev_move(self, action: models.MoveAction):
        """A testing route to simulate an input to the ui."""
        self.send_action(action)

    def dev_cast_minion(self, action: models.CastMinionAction):
        """A testing route to simulate an input to the ui."""
        self.send_action(action)

    def send_action(self, action: models.ACTION):
        self.controller._receive_action(action)
