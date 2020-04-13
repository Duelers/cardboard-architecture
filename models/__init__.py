from __future__ import annotations

import models.cell_type
import models.decks

"""All the models are in one one package in the python implementation, because it greatly simplifies circular 
dependencies in pydantic."""

import pydantic
import typing

from . import cells
from . import cards
from . import zones
from . import players

CardInstanceId = pydantic.conint(ge=0)


class CardRegistry(pydantic.BaseModel):
    """Matches cards to unique ids"""
    next_card_instance_id: CardInstanceId = 0
    instance_id_to_card: typing.Dict[CardInstanceId, cards.BaseCard] = {}

    def register(self, card: cards.BaseCard):
        card.instance_id = self.next_card_instance_id
        self._add_to_dict(card)
        self.next_card_instance_id += 1

    def get_card_by_instance_id(self, instance_id: CardInstanceId):
        return self.instance_id_to_card[instance_id]

    def _add_to_dict(self, card: cards.BaseCard):
        self._assert_not_in_dict(card)
        self.instance_id_to_card[card.instance_id] = card

    def _assert_not_in_dict(self, card: cards.BaseCard):
        try:
            card_already_with_id = self.instance_id_to_card[card.instance_id]
            assert False, f'{card_already_with_id} is already registered with id: {card.instance_id}'
        except KeyError:
            pass


ZoneOrBoardLocation = typing.Union[zones.PlayerZone, cells.BoardLocation]


class LocationRegistry(pydantic.BaseModel):
    """Matches cards to locations"""
    card_to_location: typing.Dict[CardInstanceId, ZoneOrBoardLocation] = {}

    def register(self, card: CardInstanceId, location: ZoneOrBoardLocation):
        self.card_to_location[card] = location


# INTERACTIONS (Mixins for Effects and Actions)
class _Move(pydantic.BaseModel):
    name: typing.Literal['Move'] = 'Move'
    start_cell: cells.BoardLocation
    end_cell: cells.BoardLocation


class _CastMinion(pydantic.BaseModel):
    name: typing.Literal['CastMinion'] = 'CastMinion'
    target_cell: cells.BoardLocation
    minion_instance_id: CardInstanceId


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
        game_state.move_unit(self.start_cell, self.end_cell)
        return game_state


class MoveAction(BaseAction, _Move):
    def to_effect(self, model: GameState) -> BaseEffect:
        return MoveEffect(start_cell=self.start_cell, end_cell=self.end_cell)


class CastMinionEffect(BaseEffect, _CastMinion):
    def get_animation(self, game_state: GameState):
        return f'Casting Minion {self.minion_instance_id} to {self.target_cell}'

    def update_model(self, game_state: GameState) -> GameState:
        # game_state = game_state.copy(deep=True) #check if this matters.
        minion = game_state.card_registry.get_card_by_instance_id(self.minion_instance_id)
        game_state.place_unit(unit=minion, target_cell=self.target_cell)
        return game_state


class CastMinionAction(BaseAction, _CastMinion):
    def to_effect(self, model: GameState) -> BaseEffect:
        return CastMinionEffect(target_cell=self.target_cell, minion_instance_id=self.minion_instance_id)


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
column_type = pydantic.conlist(models.cell_type.CellType,
                               min_items=cells.NUM_ROWS,
                               max_items=cells.NUM_ROWS)
board_type = pydantic.conlist(column_type,
                              min_items=cells.NUM_COLUMNS,
                              max_items=cells.NUM_COLUMNS)


class PlayerState(pydantic.BaseModel):
    deck: decks.CurrentDeck

    def zone_to_field(self, zone: zones.PLAYER_ZONE_NAMES):
        if zone == zones.Deck:
            return self.deck
        else:
            assert False
            # todo


class GameState(pydantic.BaseModel):  # todo consider splitting up.
    board: board_type = [[None for y in range(cells.NUM_ROWS)] for x in range(cells.NUM_COLUMNS)]
    some_value: int = 0
    player_1_state: PlayerState
    player_2_state: PlayerState
    listeners: typing.List[Listener] = []

    # These are technically computable and unnecessary, but convenient for the view.
    card_registry: CardRegistry
    location_registry: LocationRegistry

    def get_cell(self, cell: cells.BoardLocation) -> models.cell_type.CellType:
        return self.board[cell.x][cell.y]

    @property
    def all_cells(self) -> typing.List[models.cell_type.Cell]:
        all_cells = []
        for x in range(cells.NUM_COLUMNS):
            for y in range(cells.NUM_ROWS):
                cell = models.cell_type.Cell(column=x, row=y, contents=self.get_cell(cells.BoardLocation(x=x, y=y)))
                all_cells.append(cell)
        return all_cells

    def move_unit(self, start_cell: cells.BoardLocation, end_cell: cells.BoardLocation):
        moving_unit = self.get_cell(start_cell)
        assert moving_unit is not None, f"Cannot move a unit from {start_cell}. There is no unit there."
        self._assert_cell_empty(end_cell)

        self._set_cell(start_cell, None)
        self._set_cell(end_cell, moving_unit)

    def place_unit(self, unit: cards.UNIT, target_cell: cells.BoardLocation):
        unit_old_location: zones.PlayerZone = self.location_registry.card_to_location[unit.instance_id]
        assert isinstance(unit_old_location, zones.PlayerZone), f'unit {unit} is already on the board. Use move_unit.'
        self._remove_card_from_player_location(unit, unit_old_location)
        self._set_cell(target_cell, unit)

    def _set_cell(self, cell: cells.BoardLocation, value: models.cell_type.CellType):
        if value is not None:
            self._assert_cell_empty(cell)  # todo do in set_cell
            self.location_registry.register(value.instance_id, cell)
        self.board[cell.x][cell.y] = value

    def _assert_cell_empty(self, cell: cells.BoardLocation):
        content = self.get_cell(cell)
        assert content is None, f"Cell {cell} should be empty, but contains {content}."

    def _remove_card_from_player_location(self, card: cards.BaseCard, old_location: zones.PlayerZone):
        player_state = self._player_num_to_player_state(old_location.player)
        field = player_state.zone_to_field(old_location.zone)
        field.remove(card)

    def _player_num_to_player_state(self, player_num: players.PlayerNumber):
        if player_num == 1:
            return self.player_1_state
        else:
            assert False
        # todo


class GameUpdate(pydantic.BaseModel):
    game_state: GameState
    effect: typing.Optional[BaseEffect]
