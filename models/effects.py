import pydantic

import models.events
from . import cells


class BaseEffect(pydantic.BaseModel):
    def to_event(self, model: models.GameState) -> models.events.BaseEvent:
        return NotImplemented


class MoveEffect(BaseEffect):
    start_cell: cells.cell_index
    end_cell: cells.cell_index

    def to_event(self, model: models.GameState) -> models.events.BaseEvent:
        return models.events.MoveEvent(start_cell=self.start_cell, end_cell=self.end_cell)
