import requests
import typing
from fastapi import FastAPI

import models.events
import models.game_update
from . import game_model
import networking

app = FastAPI()


@app.post(networking.RECEIVE_GAME_STATE)
def receive_game_state(game_state: models.game_state.GameState, event: models.events.BaseEvent):
    """Updates the view's model of the game.

    Currently this is keeping the event parameter to be simpler for the sender."""
    update = models.game_update.GameUpdate(game_state=game_state, event=None)
    game_model.Model.update(update)


@app.post(networking.RECEIVE_MOVE)
def receive_move(game_state: models.game_state.GameState, event: models.events.MoveEvent):
    """Updates the view's model of the game from the sent move."""
    update = models.game_update.GameUpdate(game_state=game_state, event=event)
    game_model.Model.update(update)


@app.post(networking.DEV_USER_INPUT)
def dev_user_input():
    """A testing route to simulate an input to the ui."""
    send_user_input()


def send_user_input():
    requests.post(
        f'{networking.LOCAL_HOST}{networking.CONTROLLER_PORT}{networking.USER_INPUT}',
        params={'start_cell': '0', 'end_cell': '1'}
    )
