from fastapi import FastAPI

from . import new_game
from . import game_logic
from . import game_model
import networking
import models.effects
import models.cells

app = FastAPI()


# Todo add selection targets.

@app.post(networking.NEW_GAME)
def setup_new_game():
    """Creates a new game, and updates the view."""
    update = new_game.generate_intial_game_update()
    game_model.Model.update(update)


@app.post(networking.USER_INPUT)
def user_input(start_cell: models.cells.cell_index, end_cell: models.cells.cell_index):
    effect = models.effects.MoveEffect(start_cell=start_cell, end_cell=end_cell)
    game_logic.update_game_logic(effect)
