import typing
from fastapi import FastAPI

from .model_updater import ModelUpdater
from . import available_actions as available_actions_mod
from . import game_model
from . import load_resources
from . import networking_to_view
import networking
import models.decks

app = FastAPI()

deck_ids = ('deck0', 'deck0')  # Todo generate games programmatically.
# noinspection PyTypeChecker
master_decks: typing.Tuple[models.decks.MasterDeck, models.decks.MasterDeck] \
    = tuple(load_resources.get_master_deck(deck_id) for deck_id in deck_ids)

model = game_model.Model(master_decks)
model_updater = ModelUpdater(model)  # todo duplication with setup_new_game..


@app.post(networking.NEW_GAME)
def setup_new_game():
    """Creates a new game, and updates the view."""
    global model, model_updater
    model = game_model.Model(master_decks)
    model_updater = ModelUpdater(model)
    networking_to_view.send_game_state(model.game_state)


@app.post(networking.RECEIVE_ACTION)
def receive_action(action: models.ACTION):
    """Receive an action from the View."""
    model_updater.handle_action(action)


@app.get(networking.GET_AVAILABLE_ACTIONS,
         response_model=typing.List[models.MoveAction])
def available_actions():
    """Get all available actions."""
    available_actions = available_actions_mod.get_available_actions(model.game_state)
    return available_actions
