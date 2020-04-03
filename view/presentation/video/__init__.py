import models
from . import video_resources


def display_board(game_state: models.GameState):
    cell_to_display = {True: 'x', False: '_'}

    print('Board:')
    for row in range(models.constants.NUM_ROWS):
        display_row = []
        for column in range(models.constants.NUM_COLUMNS):
            cell = game_state.get_cell(models.cells.BoardLocation(x=column, y=row))
            display = cell_to_display[cell]
            display_row.append(display)
        print(display_row)


def play_animation(event: models.BaseEvent, game_state: models.GameState):
    print(event.get_animation(game_state))


def get_video(src):
    video = video_resources.RESOURCES[src]
    return video
