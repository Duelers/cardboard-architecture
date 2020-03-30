import json

import requests
from fastapi import FastAPI

import models.events
import models.game_update
import networking

app = FastAPI()


# Todo add selection targets.


def send_game_state(game_state: models.game_state.GameState):
    requests.post(
        f'{networking.LOCAL_HOST}{networking.VIEW_PORT}{networking.RECEIVE_GAME_STATE}',
        json=json.loads(game_state.json())
    )


def send_update(update: models.game_update.GameUpdate):
    if update.event:
        route = update.event.get_route()
    else:
        route = networking.RECEIVE_GAME_STATE
        update.event = models.events.BaseEvent()
    requests.post(
        f'{networking.LOCAL_HOST}{networking.VIEW_PORT}{route}',
        json=json.loads(update.json())
    )
