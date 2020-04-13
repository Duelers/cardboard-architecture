from __future__ import annotations

import pydantic

NUM_ROWS = 5
RowIndex = pydantic.conint(ge=0, lt=NUM_ROWS)
NUM_COLUMNS = 7
ColumnIndex = pydantic.conint(ge=0, lt=NUM_COLUMNS)


class BoardLocation(pydantic.BaseModel):
    x: ColumnIndex
    y: RowIndex


GENERAL_LOCATIONS = [BoardLocation(x=0, y=2), BoardLocation(x=NUM_COLUMNS - 1, y=2)]
