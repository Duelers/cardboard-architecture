import requests
import typing
from fastapi import FastAPI
import json
import models.cells
from . import game_model
from . import presentation
import networking

app = FastAPI()

model = game_model.Model(presentation.Presentation())


# noinspection PyUnusedLocal
@app.post(networking.RECEIVE_GAME_STATE)
def receive_game_state(game_state: models.GameState):
    """Updates the view's model of the game."""
    model.initialize(game_state)
    model.present()


# Receive effects
@app.post(networking.RECEIVE_EFFECT)
def receive_effect(game_state: models.GameState, effect: models.EFFECT):
    update = models.GameUpdate(game_state=game_state, effect=effect)
    model.update(update)


@app.post(networking.RECEIVE_AVAILABLE_ACTIONS)
def receive_available_actions(actions: typing.List[models.BaseAction]):
    print(actions)
    pass  # todo model.display_options() ?


# Temporary debug inputs to simulate having a user interface.
# @app.post(networking.DEV_SELECTION)
# def dev_selection(selection_cell: models.cells.BoardLocation):
#     """A testing route to simulate an input to the ui."""
#     send_selection(selection_cell)


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

# def send_selection(selected_cell: models.cells.BoardLocation):
#     requests.post(
#         f'{networking.LOCAL_HOST}{networking.CONTROLLER_PORT}{networking.GET_AVAILABLE_ACTIONS}',
#         json={'selected_cell': json.loads(selected_cell.json())}
#     )
