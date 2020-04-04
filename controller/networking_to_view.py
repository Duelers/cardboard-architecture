import json

import requests
from fastapi import FastAPI
import models
import networking

app = FastAPI()


def send_game_state(game_state: models.GameState):
    requests.post(
        f'{networking.LOCAL_HOST}{networking.VIEW_PORT}{networking.RECEIVE_GAME_STATE}',
        json=json.loads(game_state.json())
    )


def send_update(update: models.GameUpdate):
    route = networking.RECEIVE_EFFECT
    if not update.effect:
        update.effect = models.BaseEffect()
        route = networking.RECEIVE_GAME_STATE
    requests.post(
        f'{networking.LOCAL_HOST}{networking.VIEW_PORT}{route}',
        json=json.loads(update.json())
    )
