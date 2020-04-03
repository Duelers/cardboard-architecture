import typing

import models
import models.cells
import models.constants


def get_available_actions(game_state: models.GameState) -> typing.List[models.MoveAction]:
    all_actions = []
    for cell in game_state.all_cells:
        if cell.contents:
            actions = _get_available_actions_from_cell(models.cells.BoardLocation(x=cell.column, y=cell.row),
                                                       game_state)
            all_actions += actions
    return all_actions


def _get_available_actions_from_cell(
        cell: models.cells.BoardLocation,
        game_state: models.GameState
) -> typing.List[models.MoveAction]:
    if not game_state.get_cell(cell):
        assert False, "Nothing to move at selected cell."
    all_actions = [models.MoveAction(start_cell=cell,
                                     end_cell=(models.cells.BoardLocation(
                                         x=(cell.x + move) % models.constants.NUM_COLUMNS,
                                         y=cell.y))
                                     )
                   for move in (-1, +1)]  # todo update this
    unblocked_actions = [action for action in all_actions if not game_state.get_cell(action.end_cell)]
    return unblocked_actions
