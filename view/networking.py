import requests
from fastapi import FastAPI
import json
import models.cells
from . import game_model
import networking

app = FastAPI()

model = game_model.Model()


# noinspection PyUnusedLocal
@app.post(networking.RECEIVE_GAME_STATE)
def receive_game_state(game_state: models.GameState, effect: models.BaseEffect):
    """Updates the view's model of the game.

    Currently this is keeping the effect parameter to be simpler for the sender."""
    update = models.GameUpdate(game_state=game_state, effect=None)
    model.update(update)


# Receive effects
@app.post(networking.RECEIVE_EFFECT)
def receive_effect(game_state: models.GameState, effect: models.EFFECT):
    update = models.GameUpdate(game_state=game_state, effect=effect)
    model.update(update)


# Temporary debug inputs to simulate having a user interface.
@app.post(networking.DEV_SELECTION)
def dev_selection(selection_cell: models.cells.BoardLocation):
    """A testing route to simulate an input to the ui."""
    send_selection(selection_cell)


@app.post(networking.DEV_MOVE)
def dev_move(action: models.MoveAction):
    """A testing route to simulate an input to the ui."""
    send_action(action)


@app.post(networking.DEV_CAST_MINION)
def dev_cast_minion(action: models.CastMinionAction):
    """A testing route to simulate an input to the ui."""
    send_action(action)


def send_action(action: models.ACTION):
    requests.post(
        f'{networking.LOCAL_HOST}{networking.CONTROLLER_PORT}{networking.RECEIVE_ACTION}',
        json=json.loads(action.json())
    )


def send_selection(selected_cell: models.cells.BoardLocation):
    requests.post(
        f'{networking.LOCAL_HOST}{networking.CONTROLLER_PORT}{networking.GET_AVAILABLE_ACTIONS}',
        json={'selected_cell': json.loads(selected_cell.json())}
    )
