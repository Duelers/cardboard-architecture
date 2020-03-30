import models.events
from . import video_resources


def display_board(game_state: models.GameState):
    cell_to_display = {True: 'x', False: '_'}
    cell_displays = [cell_to_display[cell] for cell in game_state.board]
    print(f'Board: {"".join(cell_displays)}')


def play_animation(event: models.events.BaseEvent):
    print(event.get_animation())


def get_video(src):
    video = video_resources.RESOURCES[src]
    return video
