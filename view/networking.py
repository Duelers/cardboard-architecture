import requests
from fastapi import FastAPI
import json
import models.cells
from . import game_model
import networking

app = FastAPI()

model = game_model.Model()


@app.post(networking.RECEIVE_GAME_STATE)
def receive_game_state(game_state: models.GameState, effect: models.BaseEffect):
    """Updates the view's model of the game.

    Currently this is keeping the effect parameter to be simpler for the sender."""
    update = models.GameUpdate(game_state=game_state, effect=None)
    model.update(update)


@app.post(networking.RECEIVE_MOVE)
def receive_move(game_state: models.GameState, effect: models.MoveEffect):
    """Updates the view's model of the game from the sent move."""
    update = models.GameUpdate(game_state=game_state, effect=effect)
    model.update(update)


@app.post(networking.RECEIVE_CHANGE_SOME_VALUE)
def receive_change_some_value(game_state: models.GameState, effect: models.ChangeSomeValueEffect):
    """Updates the view's model of the game from the sent move."""
    update = models.GameUpdate(game_state=game_state, effect=effect)
    model.update(update)


@app.post(networking.DEV_SELECTION)
def dev_selection(selection_cell: models.cells.BoardLocation):
    """A testing route to simulate an input to the ui."""
    send_selection(selection_cell)


@app.post(networking.DEV_USER_INPUT)
def dev_user_input(start_cell: models.cells.BoardLocation, end_cell: models.cells.BoardLocation):
    """A testing route to simulate an input to the ui."""
    send_user_input(start_cell, end_cell)


def send_user_input(start_cell: models.cells.BoardLocation, end_cell: models.cells.BoardLocation):
    requests.post(
        f'{networking.LOCAL_HOST}{networking.CONTROLLER_PORT}{networking.USER_INPUT}',
        json={'start_cell': json.loads(start_cell.json()),
              'end_cell': json.loads(end_cell.json())}
    )


def send_selection(selected_cell: models.cells.BoardLocation):
    requests.post(
        f'{networking.LOCAL_HOST}{networking.CONTROLLER_PORT}{networking.GET_AVAILABLE_ACTIONS}',
        json={'selected_cell': json.loads(selected_cell.json())}
    )
