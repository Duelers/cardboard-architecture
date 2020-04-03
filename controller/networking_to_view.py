import json

import requests
from fastapi import FastAPI
import models
import networking

app = FastAPI()


# Todo add selection targets.


def send_game_state(game_state: models.GameState):
    requests.post(
        f'{networking.LOCAL_HOST}{networking.VIEW_PORT}{networking.RECEIVE_GAME_STATE}',
        json=json.loads(game_state.json())
    )


def send_update(update: models.GameUpdate):
    if update.effect:
        route = update.effect.get_route()
    else:
        route = networking.RECEIVE_GAME_STATE
        update.effect = models.BaseEffect()
    requests.post(
        f'{networking.LOCAL_HOST}{networking.VIEW_PORT}{route}',
        json=json.loads(update.json())
    )
