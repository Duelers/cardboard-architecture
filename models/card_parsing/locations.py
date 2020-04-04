from __future__ import annotations

import pydantic

import base
import typing

# Location
this = "this"


class LocationFromCoords(base.BaseModel):
    name: typing.Literal['location_from_coords']
    row: pydantic.conint(ge=0, le=4)
    col: pydantic.conint(ge=0, le=8)


class LocationFromUnit(base.BaseModel):  # uses Object
    name: typing.Literal['location_from_unit']
    unit: objects.Object


class GetVarLocation(base.BaseModel):
    name: typing.Literal['get_var_location']
    var: str


class ChooseLocation(base.BaseModel):  # Requires Locations
    name: typing.Literal['choose_location']
    choose_from: Locations


class ChooseRandom(base.BaseModel):  # Requires Locations
    name: typing.Literal['choose_random']
    choose_from: Locations  # todo, make this work for more types


# Locations
everywhere = 'everywhere'
walkable = 'walkable'


class Row(base.BaseModel):
    name: typing.Literal['row']
    row: pydantic.conint(ge=0, le=4)


class Column(base.BaseModel):
    name: typing.Literal['column']
    col: pydantic.conint(ge=0, le=8)


class AdjacentToLocation(base.BaseModel):  # Uses Location
    name: typing.Literal['adjacent_to_location']
    location: Location


class UnionLocations(base.BaseModel):  # Uses Locations
    name: typing.Literal['union_locations']
    left: Locations
    right: Locations


class SubtractLocations(base.BaseModel):
    name: typing.Literal['subtract_locations']
    left: Locations
    right: Locations


Location = typing.Union[typing.Literal[this],
                        LocationFromCoords,
                        LocationFromUnit,
                        GetVarLocation,
                        ChooseLocation,
                        ChooseRandom]

Locations = typing.Union[Location,
                         typing.Literal[everywhere],
                         typing.Literal[walkable],
                         Row,
                         Column,
                         AdjacentToLocation,
                         UnionLocations,
                         SubtractLocations
]

import objects

LocationFromUnit.update_forward_refs()
ChooseLocation.update_forward_refs()
UnionLocations.update_forward_refs()
AdjacentToLocation.update_forward_refs()
UnionLocations.update_forward_refs()
SubtractLocations.update_forward_refs()
ChooseRandom.update_forward_refs()
