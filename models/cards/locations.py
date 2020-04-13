from __future__ import annotations

import abc

import typing

from . import base

import models.cells
from .base import GetterType

if typing.TYPE_CHECKING:
    import models
    from . import InGameCardMixin


class SingleLocation(base.SingleGetter[models.cells.BoardLocation], abc.ABC):
    pass


class MultipleLocation(base.MultipleGetter[models.cells.BoardLocation], abc.ABC):
    pass


class LocationFromCoords(SingleLocation):
    row: models.cells.RowIndex
    col: models.cells.ColumnIndex

    def get(self, game_state: models.GameState, this: models.cards.BaseCard):
        import models
        return models.cells.BoardLocation(x=self.col, y=self.row)


class This(SingleLocation):
    def get(self, game_state: models.GameState, this: models.cards.BaseCard):
        unit = objects.This().get(game_state, this)
        location = game_state.location_registry.card_to_location[unit.instance_id]
        return location


class LocationFromUnit(SingleLocation):  # uses Object
    unit: objects.Unit

    def get(self, game_state: models.GameState, this: InGameCardMixin):
        location = game_state.location_registry.card_to_location[this.instance_id]
        return location


class GetVarLocation(SingleLocation):
    var: str

    def get(self, game_state: models.GameState, this: models.cards.BaseCard):
        pass


class ChooseLocation(SingleLocation):  # Requires Locations
    choose_from: MultipleLocation

    def get(self, game_state: models.GameState, this: models.cards.BaseCard):
        pass


class ChooseRandom(SingleLocation):  # Requires Locations
    choose_from: typing.List[SingleLocation]  # todo, make this a generic.

    def get(self, game_state: models.GameState, this: models.cards.BaseCard):
        pass


# Locations

class Everywhere(MultipleLocation):
    def get_multiple(self, game_state: models.GameState, this: models.cards.BaseCard) -> typing.List[GetterType]:
        pass


class Walkable(MultipleLocation):
    def get_multiple(self, game_state: models.GameState, this: models.cards.BaseCard) -> typing.List[GetterType]:
        pass


class Row(MultipleLocation):
    row: models.cells.RowIndex

    def get_multiple(self, game_state: models.GameState, this: models.cards.BaseCard) -> typing.List[GetterType]:
        pass


class Column(MultipleLocation):
    col: models.cells.ColumnIndex

    def get_multiple(self, game_state: models.GameState, this: models.cards.BaseCard) -> typing.List[GetterType]:
        pass


class AdjacentToLocation(MultipleLocation):  # Uses Location
    location: SingleLocation

    def get_multiple(self, game_state: models.GameState, this: models.cards.BaseCard) -> typing.List[GetterType]:
        pass


class UnionLocations(MultipleLocation):  # Uses Locations
    left: MultipleLocation
    right: MultipleLocation

    def get_multiple(self, game_state: models.GameState, this: models.cards.BaseCard) -> typing.List[GetterType]:
        pass


class SubtractLocations(MultipleLocation):
    left: MultipleLocation
    right: MultipleLocation

    def get_multiple(self, game_state: models.GameState, this: models.cards.BaseCard) -> typing.List[GetterType]:
        pass


from . import objects

LocationFromCoords.update_forward_refs()
LocationFromUnit.update_forward_refs()
ChooseLocation.update_forward_refs()
UnionLocations.update_forward_refs()
AdjacentToLocation.update_forward_refs()
UnionLocations.update_forward_refs()
SubtractLocations.update_forward_refs()
ChooseRandom.update_forward_refs()
