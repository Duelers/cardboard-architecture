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

        self.available_actions = None

    def set_view(self, view):
        """Must be called before use."""
        self.view = view

    def setup_new_game(self, master_decks):
        """Creates a new game, and updates the view."""
        # noinspection PyTypeChecker
        self.model = game_model.Model(master_decks, self.view.receive_update)
        self.model_updater = ModelUpdater(self.model)
        self.send_game_state(self.model.game_state)

    def receive_choice(self, choice: int):
        """Receives a choice from the view. This is how the view communicates to the controller."""
        action = self.available_actions[choice]  # todo make this work for other kinds of choices based on context.
        self._receive_action(action)

    def _receive_action(self, action: models.ACTION):
        """Receive an action from the View."""
        update = self.model_updater.handle_action(action)
        self.send_update(update)
        self.send_available_actions()

    def send_available_actions(self):
        """Sends all available actions."""
        self.available_actions = available_actions_mod.get_available_actions(self.model.game_state)
        self.view.receive_available_actions(self.available_actions)

    def send_game_state(self, game_state: models.GameState):
        """Sends the game state without an Effect for some reason, such as when the game first loads."""
        self.view.receive_game_state(game_state)

    def send_update(self, update: models.GameUpdate):
        """Sends a game update with an attached Effect if there is one."""
        if update.effect:
            self.view.receive_update(update)
        else:
            self.send_game_state(update.game_state)
