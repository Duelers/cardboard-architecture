import pydantic
import typing

from . import constants

cell_type = bool

row_index = pydantic.conint(ge=0, lt=constants.NUM_ROWS)
column_index = pydantic.conint(ge=0, lt=constants.NUM_COLUMNS)
# board_index = typing.Tuple[row_index, column_index]
class BoardLocation(pydantic.BaseModel):
    x: column_index
    y: row_index

row_cell_type = pydantic.conint(ge=0, lt=constants.NUM_ROWS)
column_cell_type = pydantic.conint(ge=0, lt=constants.NUM_COLUMNS)



class Cell(pydantic.BaseModel):
    row: row_cell_type
    column: column_cell_type
    contents: cell_type
