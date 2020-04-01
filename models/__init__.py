from __future__ import annotations

"""All the models are in one one package in the python implementation, because it greatly simplifies circular 
dependencies in pydantic."""

import pydantic
import typing

from . import cells
from . import constants

from . import cells
import networking


# EVENTS
class BaseEvent(pydantic.BaseModel):
    def get_animation(self, game_state: GameState):
        return NotImplemented

    def update_model(self, game_state: GameState) -> GameState:
        return NotImplemented

    def get_route(self) -> str:
        return NotImplemented


class MoveEvent(BaseEvent):
    start_cell: cells.cell_index
    end_cell: cells.cell_index

    def get_animation(self, game_state: GameState):
        return f'Moving from {self.start_cell} to {self.end_cell}'

    def update_model(self, game_state: GameState) -> GameState:
        game_state = game_state.copy(deep=True)
        game_state.board[self.start_cell] = False
        game_state.board[self.end_cell] = True
        return game_state

    def get_route(self) -> str:
        return networking.RECEIVE_MOVE


class ChangeSomeValueEvent(BaseEvent):
    increase_by: int

    def get_animation(self, game_state: GameState):
        return f'Increasing some value by {self.increase_by}. Now {game_state.some_value}.'

    def update_model(self, game_state: GameState) -> GameState:
        game_state.some_value += self.increase_by
        return game_state

    def get_route(self) -> str:
        return networking.RECEIVE_CHANGE_SOME_VALUE


# EFFECTS
class BaseEffect(pydantic.BaseModel):
    def to_event(self, model: GameState) -> BaseEvent:
        return NotImplemented


class MoveEffect(BaseEffect):
    start_cell: cells.cell_index
    end_cell: cells.cell_index

    def to_event(self, model: GameState) -> BaseEvent:
        return MoveEvent(start_cell=self.start_cell, end_cell=self.end_cell)


class ChangeSomeValueEffect(BaseEffect):
    increase_by: int

    def to_event(self, model: GameState) -> BaseEvent:
        return ChangeSomeValueEvent(increase_by=self.increase_by)


# Listeners
class Listener(pydantic.BaseModel):
    trigger_event_type: str  # typing.Type[BaseEvent] #This breaks for an unknown reason. Issue with fastapi?
    response_effects: typing.List[BaseEffect]


board_type = pydantic.conlist(bool,
                              min_items=constants.NUM_COLUMNS,
                              max_items=constants.NUM_COLUMNS)  # board is 1x3 ints


class GameState(pydantic.BaseModel):
    board: board_type
    some_value: int
    listeners: typing.List[Listener]

    @classmethod
    def new_game(cls):
        """Constructor for default initial game state."""

        listener = Listener(trigger_event_type='MoveEvent',
                            response_effects=[
                                ChangeSomeValueEffect(increase_by=1)
                            ])

        return cls(board=[True, False, False],
                   some_value=0,
                   listeners=[listener])


class GameUpdate(pydantic.BaseModel):
    game_state: GameState
    event: typing.Optional[BaseEvent]
