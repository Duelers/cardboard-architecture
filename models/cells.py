import pydantic
from . import constants

cell_index = pydantic.conint(ge=0, lt=constants.NUM_COLUMNS)

row_cell_type = pydantic.conint(ge=0, lt=constants.NUM_ROWS)
column_cell_type = pydantic.conint(ge=0, lt=constants.NUM_COLUMNS)


class Cell(pydantic.BaseModel):
    row: row_cell_type
    column: column_cell_type
