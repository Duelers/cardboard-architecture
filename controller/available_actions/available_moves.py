import typing

import pydantic

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


def _get_available_moves_from_cell(cell: models.cells.BoardLocation, game_state: models.GameState
                                   ) -> typing.List[models.MoveAction]:
    if not game_state.get_cell(cell):
        assert False, "Nothing to move at selected cell."

    displacements = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    end_cells = []
    for displacement in displacements:
        try:
            end_cell = models.cells.BoardLocation(
                x=cell.x + displacement[0],
                y=cell.y + displacement[1])
            end_cells.append(end_cell)
        except pydantic.ValidationError:
            pass  # out of bounds, don't add to available actions.

    all_actions = [models.MoveAction(start_cell=cell, end_cell=end_cell) for end_cell in end_cells]
    unblocked_actions = [action for action in all_actions if not game_state.get_cell(action.end_cell)]
    return unblocked_actions