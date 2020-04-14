import pprint

import models.cells
from . import video_resources


def display_board(game_state: models.GameState):
    print('Board:')
    for row in range(models.cells.NUM_ROWS):
        display_row = []
        for column in range(models.cells.NUM_COLUMNS):
            cell = game_state.get_cell(models.cells.BoardLocation(x=column, y=row))
            if cell:
                display = cell.name[0]
            else:
                display = '_'
            display_row.append(display)
        print(display_row)


def display_deck(game_state: models.GameState):
    print('My Deck:')
    for card in game_state.player_1_state.deck:
        pprint.pp(card)


def play_animation(effect: models.BaseEffect, game_state: models.GameState):
    print(effect.get_animation(game_state))


def get_video(src):
    video = video_resources.RESOURCES[src]
    return video
