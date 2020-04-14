import typing

from . import available_actions as available_actions_mod
from .model_updater import ModelUpdater
from . import game_model
from . import load_resources
import models.decks

if typing.TYPE_CHECKING:
    import view


class Controller:
    def __init__(self):
        self.model = None
        self.model_updater = None

        self.view: view.View = None  # Must be set before use.

    def set_view(self, view):
        """Must be called before use."""
        self.view = view

    def start(self, master_decks):
        self.setup_new_game(master_decks)

        while True:
            action = self.request_action()
            self._perform_action(action)

    def setup_new_game(self, master_decks):
        """Creates a new game, and updates the view."""
        # noinspection PyTypeChecker
        self.model = game_model.Model(master_decks, self.view.receive_update)
        self.model_updater = ModelUpdater(self.model)
        self.send_game_state(self.model.game_state)

    def request_action(self):
        """Sends all available actions."""
        available_actions = available_actions_mod.get_available_actions(self.model.game_state, self.request_choice)
        return self.request_choice(available_actions)

    def request_choice(self, choices, description="Make a selection"):
        choice_number = self.view.receive_choices(choices, description)
        return choices[choice_number]

    def _perform_action(self, action: models.ACTION):
        """Receive an action from the View."""
        update = self.model_updater.handle_action(action)
        self.send_update(update)
        self.request_action()

    def send_game_state(self, game_state: models.GameState):
        """Sends the game state without an Effect for some reason, such as when the game first loads."""
        self.view.receive_game_state(game_state)

    def send_update(self, update: models.GameUpdate):
        """Sends a game update with an attached Effect if there is one."""
        if update.effect:
            self.view.receive_update(update)
        else:
            self.send_game_state(update.game_state)
