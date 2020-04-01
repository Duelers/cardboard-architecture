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
    update = models.GameUpdate(game_state=game_state, event=None)
    model.update(update)


@app.post(networking.USER_INPUT)
def user_input(start_cell: models.cells.cell_index, end_cell: models.cells.cell_index):
    """Receive user input."""
    effect = models.MoveEffect(start_cell=start_cell, end_cell=end_cell)
    model_updater.handle_effect(effect)


@app.get(networking.GET_AVAILABLE_ACTIONS,
         response_model=typing.List[models.MoveEffect])
def user_input():
    """Get all available actions."""
    available_effects = available_actions_generator.get_available_effects(model.get())
    return available_effects
