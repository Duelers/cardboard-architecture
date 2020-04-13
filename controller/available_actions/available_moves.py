import typing

import models
import models.cells


def get_available_moves(game_state: models.GameState) -> typing.List[models.MoveAction]:
    all_moves = []
    for cell in game_state.all_cells:
        if cell.contents:
            moves = _get_available_moves_from_cell(models.cells.BoardLocation(x=cell.column, y=cell.row),
                                                   game_state)
            all_moves += moves
    return all_moves


def _get_available_moves_from_cell(
        cell: models.cells.BoardLocation,
        game_state: models.GameState
) -> typing.List[models.MoveAction]:
    """Get moves for the unit in the cell. Requires that there is a unit in the cell."""
    content = game_state.get_cell(cell)
    if not content:
        assert False, "Nothing to move at selected cell."

    end_cells: typing.List[models.cells.BoardLocation] = content.move_options.get_list(game_state, content)
    all_actions = [models.MoveAction(start_cell=cell, end_cell=end_cell) for end_cell in end_cells]
    unblocked_actions = [action for action in all_actions if not game_state.get_cell(action.end_cell)]

    return unblocked_actions
