import pydantic

from . import constants

# row_type = pydantic.conlist(Cell, min_items=constants.NUM_ROWS, max_items=constants.NUM_ROWS)
# board_type = pydantic.conlist(row_type, min_items=constants.NUM_COLUMNS, max_items=constants.NUM_COLUMNS)
board_type = pydantic.conlist(bool, min_items=constants.NUM_COLUMNS,
                              max_items=constants.NUM_COLUMNS)  # board is 1x3 ints


class GameState(pydantic.BaseModel):
    board: board_type
