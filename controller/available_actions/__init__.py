import typing

import models.cells
from controller.available_actions.available_moves import get_available_moves


def get_available_actions(game_state: models.GameState) -> typing.List[models.BaseAction]:
    moves = get_available_moves(game_state)
    minion_casts = get_available_minion_casts(game_state)
    return moves


def get_available_minion_casts(game_state) -> typing.List[models.CastMinionAction]:
    cards = game_state.player_1_state.deck  # todo cast from hand instead of deck.

    minion_casts = []
    for card in cards:
        pass #todo allow placing in any space adjacent to a friendly minion, or something.
    return minion_casts
