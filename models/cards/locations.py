from __future__ import annotations

import abc

import typing

from . import base

import models.cells
from .base import GetterType, GetterParams

if typing.TYPE_CHECKING:
    import models
    from . import InGameCardMixin

SingleLocation = base.SingleGetter[models.cells.BoardLocation]

MultipleLocation = base.MultipleGetter[models.cells.BoardLocation]


class LocationFromCoords(SingleLocation):
    row: models.cells.RowIndex
    col: models.cells.ColumnIndex

    def get(self, params: GetterParams):
        import models
        return models.cells.BoardLocation(x=self.col, y=self.row)


class LocationFromOffset(MultipleLocation):  # multiple because that allows an empty list? NullableLocation?
    origin: SingleLocation
    row_offset: int
    column_offset: int

    def get_multiple(self, params: GetterParams):
        origin = self.origin.get(game_state, this)
        try:
            new_location = models.cells.BoardLocation(x=origin.x + self.column_offset,
                                                      y=origin.y + self.row_offset)
            return [new_location]
        except ValueError:
            return []


class This(SingleLocation):
    def get(self, params: GetterParams):
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

    def get(self, params: GetterParams):
        assert False


class ChooseLocation(base.SingleGetter[models.cells.BoardLocation]):  # Requires Locations
    choose_from: MultipleLocation

    def get(self, params: GetterParams):
        choices = self.choose_from.get_multiple(params)
        choice = params.request_choice(choices, "Choose a location")
        return choice


class ChooseRandom(SingleLocation):  # Requires Locations
    choose_from: typing.List[SingleLocation]  # todo, make this a generic.

    def get(self, params: GetterParams):
        assert False


# Locations

class Everywhere(MultipleLocation):
    def get_multiple(self, params: GetterParams) -> typing.List[GetterType]:
        assert False


class Walkable(MultipleLocation):
    def get_multiple(self, params: GetterParams) -> typing.List[GetterType]:
        assert False


class Row(MultipleLocation):
    row: models.cells.RowIndex

    def get_multiple(self, params: GetterParams) -> typing.List[GetterType]:
        locations = [models.cells.BoardLocation(x=x, y=self.row) for x in range(models.cells.NUM_COLUMNS)]
        return locations


class Column(MultipleLocation):
    col: models.cells.ColumnIndex

    def get_multiple(self, params: GetterParams) -> typing.List[GetterType]:
        locations = [models.cells.BoardLocation(x=self.col, y=y) for y in range(models.cells.NUM_ROWS)]
        return locations


class AdjacentToLocation(MultipleLocation):  # Uses Location
    location: SingleLocation

    def get_multiple(self, params: GetterParams) -> typing.List[GetterType]:
        assert False


class UnionLocations(MultipleLocation):  # Uses Locations
    locations: typing.List[MultipleLocation]

    def get_multiple(self, params: GetterParams) -> typing.List[GetterType]:
        union_locations = []
        for getter in self.locations:
            locations = getter.get_multiple(params)
            union_locations += locations
        return union_locations


class SubtractLocations(MultipleLocation):
    left: MultipleLocation
    right: MultipleLocation

    def get_multiple(self, params: GetterParams) -> typing.List[GetterType]:
        assert False


from . import objects

LocationFromCoords.update_forward_refs()
LocationFromUnit.update_forward_refs()
ChooseLocation.update_forward_refs()
UnionLocations.update_forward_refs()
AdjacentToLocation.update_forward_refs()
UnionLocations.update_forward_refs()
SubtractLocations.update_forward_refs()
ChooseRandom.update_forward_refs()
