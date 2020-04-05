import typing
from fastapi import FastAPI

from .model_updater import ModelUpdater
from . import available_actions_generator
from . import game_model
from . import load_resources
from . import networking_to_view
import networking
import models.cells
import models.decks

app = FastAPI()

deck_id = 'deck0'  # Todo generate games programmatically.
my_deck = load_resources.get_master_deck(deck_id)

model = game_model.Model(my_deck)
model_updater = ModelUpdater(model)  # todo duplication with setup_new_game..


@app.post(networking.NEW_GAME)
def setup_new_game():
    """Creates a new game, and updates the view."""
    global model, model_updater
    model = game_model.Model(my_deck)
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
    available_actions = available_actions_generator.get_available_actions(model.game_state)
    return available_actions
