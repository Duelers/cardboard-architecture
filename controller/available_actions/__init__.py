import typing

import models.cells
from controller.available_actions.available_moves import get_available_moves


def get_available_actions(game_state: models.GameState, request_choice) -> typing.List[models.BaseAction]:
    moves = get_available_moves(game_state, request_choice)
    minion_casts = get_available_minion_casts(game_state)
    return moves


def get_available_minion_casts(game_state: models.GameState) -> typing.List[models.CastMinionAction]:
    cards = game_state.player_1_state.deck.cards  # todo cast from hand instead of deck.

    minion_casts = []
    for card in cards:
        if type(card) == models.cards.Minion:
            casts = get_available_minion_casts_for_minion(game_state, card)
            minion_casts += casts
    return minion_casts


def get_available_minion_casts_for_minion(game_state: models.GameState, minion: models.cards.Minion
                                          ) -> typing.List[models.CastMinionAction]:
    return []  # todo
