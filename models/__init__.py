from __future__ import annotations

import models.decks

"""All the models are in one one package in the python implementation, because it greatly simplifies circular 
dependencies in pydantic."""

import pydantic
import typing

from . import cells
from . import cards


# INTERACTIONS (Mixins for Effects and Actions)
class _Move(pydantic.BaseModel):
    name: typing.Literal['Move'] = 'Move'
    start_cell: cells.BoardLocation
    end_cell: cells.BoardLocation


class _CastMinion(pydantic.BaseModel):
    name: typing.Literal['CastMinion'] = 'CastMinion'
    target_cell: cells.BoardLocation
    minion: cards.Minion


class _ChangeSomeValue(pydantic.BaseModel):
    name: typing.Literal['ChangeSomeValue'] = 'ChangeSomeValue'
    increase_by: int


# EFFECTS
class BaseEffect(pydantic.BaseModel):
    name: str = None  # Set to a literal in subclasses so that they can be deserialized to back to the right model.

    def get_animation(self, game_state: GameState):
        return NotImplemented

    def update_model(self, game_state: GameState) -> GameState:
        return NotImplemented


class BaseAction(pydantic.BaseModel):
    def to_effect(self, model: GameState) -> BaseEffect:
        return NotImplemented


class MoveEffect(BaseEffect, _Move):
    def get_animation(self, game_state: GameState):
        return f'Moving from {self.start_cell} to {self.end_cell}'

    def update_model(self, game_state: GameState) -> GameState:
        game_state = game_state.copy(deep=True)

        moving_unit = game_state.get_cell(self.start_cell)
        game_state.set_cell(self.start_cell, None)
        game_state.set_cell(self.end_cell, moving_unit)
        return game_state


class MoveAction(BaseAction, _Move):
    def to_effect(self, model: GameState) -> BaseEffect:
        return MoveEffect(start_cell=self.start_cell, end_cell=self.end_cell)


class CastMinionEffect(BaseEffect, _CastMinion):
    def get_animation(self, game_state: GameState):
        return f'Casting Minion {self.minion} to {self.target_cell}'

    def update_model(self, game_state: GameState) -> GameState:
        game_state = game_state.copy(deep=True)
        game_state.set_cell(self.target_cell, self.minion)
        return game_state


class CastMinionAction(BaseAction, _CastMinion):
    def to_effect(self, model: GameState) -> BaseEffect:
        return CastMinionEffect(target_cell=self.target_cell, minion=self.minion)


class ChangeSomeValueEffect(BaseEffect, _ChangeSomeValue):
    def get_animation(self, game_state: GameState):
        return f'Increasing some value by {self.increase_by}. Now {game_state.some_value}.'

    def update_model(self, game_state: GameState) -> GameState:
        game_state.some_value += self.increase_by
        return game_state


class ChangeSomeValueAction(BaseAction, _ChangeSomeValue):
    def to_effect(self, model: GameState) -> BaseEffect:
        return ChangeSomeValueEffect(increase_by=self.increase_by)


EFFECT = typing.Union[MoveEffect, CastMinionEffect, ChangeSomeValueEffect]
ACTION = typing.Union[MoveAction, CastMinionAction, ChangeSomeValueAction]


# Listeners
class Listener(pydantic.BaseModel):
    trigger_effect_type: str  # typing.Type[BaseEffect] #This breaks for an unknown reason. Issue with fastapi?
    response_actions: typing.List[BaseAction]


# board[x][y] = cells.cell_type
# board[x] = List3[bool] (Column)
# board = List3[Column] (Board)
column_type = pydantic.conlist(cells.cell_type,
                               min_items=cells.NUM_ROWS,
                               max_items=cells.NUM_ROWS)
board_type = pydantic.conlist(column_type,
                              min_items=cells.NUM_COLUMNS,
                              max_items=cells.NUM_COLUMNS)


class GameState(pydantic.BaseModel):
    board: board_type
    some_value: int
    listeners: typing.List[Listener]

    def get_cell(self, location: cells.BoardLocation) -> cells.cell_type:
        return self.board[location.x][location.y]

    def set_cell(self, location: cells.BoardLocation, value: cells.cell_type):
        self.board[location.x][location.y] = value

    @property
    def all_cells(self) -> typing.List[cells.Cell]:
        all_cells = []
        for x in range(cells.NUM_COLUMNS):
            for y in range(cells.NUM_ROWS):
                cell = cells.Cell(column=x, row=y, contents=self.get_cell(cells.BoardLocation(x=x, y=y)))
                all_cells.append(cell)
        return all_cells

    @classmethod
    def new_game(cls, my_deck: models.decks.Deck):
        """Constructor for default initial game state."""

        listener = Listener(trigger_effect_type='MoveEffect',
                            response_actions=[
                                ChangeSomeValueAction(increase_by=1)
                            ])

        my_general = my_deck.general

        board = [[None, None, my_general, None, None],
                 [None, None, None, None, None],
                 [None, None, None, None, None],
                 [None, None, None, None, None],
                 [None, None, None, None, None],
                 [None, None, None, None, None],
                 [None, None, None, None, None]]

        new_game_state = cls(board=board,
                             some_value=0,
                             listeners=[listener])

        return new_game_state


class GameUpdate(pydantic.BaseModel):
    game_state: GameState
    effect: typing.Optional[BaseEffect]
