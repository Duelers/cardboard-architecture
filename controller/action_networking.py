import json
import typing

import pydantic
import requests
from fastapi import FastAPI

import models
from .model_updater import ModelUpdater
from . import available_actions as available_actions_mod
from . import game_model
from . import load_resources
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
    send_game_state(model.game_state)


@app.post(networking.RECEIVE_ACTION)
def receive_action(action: models.ACTION):
    """Receive an action from the View."""
    model_updater.handle_action(action)

    send_available_actions()


@app.post(networking.DEV_SEND_AVAILABLE_ACTIONS)
def dev_send_available_actions():
    send_available_actions()


def _send_message(content: typing.Union[pydantic.BaseModel, typing.List[pydantic.BaseModel]], route: str):
    try:
        json_data = json.loads(content.json())
    except AttributeError:
        json_data = [item.json() for item in content]
    requests.post(
        f'{networking.LOCAL_HOST}{networking.VIEW_PORT}{route}',
        json=json_data
    )


def send_available_actions():
    """Sends all available actions."""
    available_actions: typing.List[models.BaseAction] = available_actions_mod.get_available_actions(model.game_state)
    _send_message(available_actions, networking.RECEIVE_AVAILABLE_ACTIONS)
    # requests.post(
    #     f'{networking.LOCAL_HOST}{networking.VIEW_PORT}{networking.GET_AVAILABLE_ACTIONS}',
    #     json=json.loads(available_actions)
    # )


def send_game_state(game_state: models.GameState):
    """Sends the game state without an Effect for some reason, such as when the game first loads."""
    _send_message(game_state, networking.RECEIVE_GAME_STATE)
    # requests.post(
    #     f'{networking.LOCAL_HOST}{networking.VIEW_PORT}{networking.RECEIVE_GAME_STATE}',
    #     json=json.loads(game_state.json())
    # )


def send_update(update: models.GameUpdate):
    """Sends a game update with an attached Effect if there is one."""
    if update.effect:
        _send_message(update, networking.RECEIVE_EFFECT)
        # requests.post(
        #     f'{networking.LOCAL_HOST}{networking.VIEW_PORT}{networking.RECEIVE_EFFECT}',
        #     json=json.loads(update.json())
        # )
    else:
        send_game_state(update.game_state)
