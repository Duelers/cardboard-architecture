import typing

import pydantic

from models import cards
from models.cells import RowIndex, ColumnIndex

CellType = typing.Optional[cards.InGameUnit]


class Cell(pydantic.BaseModel):
    """Used to view a cell in a collection of Cells. Not used in storage."""
    row: RowIndex
    column: ColumnIndex
    contents: CellType
