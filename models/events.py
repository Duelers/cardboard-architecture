import pydantic

from . import cells
import models
import networking


class BaseEvent(pydantic.BaseModel):
    def get_animation(self):
        return NotImplemented

    def update_model(self, model: models.GameState) -> models.GameState:
        return NotImplemented

    def get_route(self) -> str:
        return NotImplemented


class MoveEvent(BaseEvent):
    start_cell: cells.cell_index
    end_cell: cells.cell_index

    def get_animation(self):
        return f'Moving from {self.start_cell} to {self.end_cell}'

    def update_model(self, model: models.GameState) -> models.GameState:
        model.board[self.start_cell] = False
        model.board[self.end_cell] = True
        return model

    def get_route(self) -> str:
        return networking.RECEIVE_MOVE
