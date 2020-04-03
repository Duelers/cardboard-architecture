import pydantic

cell_type = bool

NUM_ROWS = 3
row_index = pydantic.conint(ge=0, lt=NUM_ROWS)
NUM_COLUMNS = 3
column_index = pydantic.conint(ge=0, lt=NUM_COLUMNS)


# board_index = typing.Tuple[row_index, column_index]
class BoardLocation(pydantic.BaseModel):
    x: column_index
    y: row_index


row_cell_type = pydantic.conint(ge=0, lt=NUM_ROWS)
column_cell_type = pydantic.conint(ge=0, lt=NUM_COLUMNS)


class Cell(pydantic.BaseModel):
    row: row_cell_type
    column: column_cell_type
    contents: cell_type
