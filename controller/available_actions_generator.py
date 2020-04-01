import typing

import models
import models.cells
import models.constants


def get_available_effects(game_state: models.GameState) -> typing.List[models.MoveEffect]:
    all_effects = []
    for cell_i, has_unit in enumerate(game_state.board):
        if has_unit:
            effects = _get_available_effects_from_cell(cell_i, game_state)
            all_effects += effects
    return all_effects


def _get_available_effects_from_cell(
        cell: models.cells.cell_index,
        game_state: models.GameState
) -> typing.List[models.MoveEffect]:
    if not game_state.board[cell]:
        assert False, "Nothing to move at selected cell."
    all_effects = [models.MoveEffect(start_cell=cell,
                                     end_cell=(cell + move) % models.constants.NUM_COLUMNS)
                   for move in (-1, +1)]
    unblocked_effects = [effect for effect in all_effects if not game_state.board[effect.end_cell]]
    return unblocked_effects
