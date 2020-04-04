import typing
from fastapi import FastAPI

from .model_updater import ModelUpdater
from . import available_actions_generator
from . import game_model
import networking
import models.cells

app = FastAPI()

model = game_model.Model()
model_updater = ModelUpdater(model)


@app.post(networking.NEW_GAME)
def setup_new_game():
    """Creates a new game, and updates the view."""
    game_state = models.GameState.new_game()
    update = models.GameUpdate(game_state=game_state, effect=None)
    model.update(update)


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
