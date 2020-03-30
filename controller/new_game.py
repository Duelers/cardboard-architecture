import models
import models.game_update


def generate_intial_game_update() -> models.game_update.GameUpdate:
    game_state = generate_initial_game_state()
    event = None
    update = models.game_update.GameUpdate(
        game_state=game_state,
        event=event)
    return update


def generate_initial_game_state() -> models.GameState:
    game_state = models.GameState(
        board=[True, False, False]
    )
    return game_state
