from __future__ import annotations

import typing
from typing import Union

import locations
import objects
import players
import base

import properties
import operators
import events


class EffectModel(base.BaseModel):
    description: str = None


class DrawCards(EffectModel):
    """Add cards from the player's deck to their hand."""
    name: typing.Literal['draw_cards']
    player: players.Player = players.you
    num_cards: int = 1


class SetVarObject(EffectModel):
    """Define a scripting variables to the given object."""
    name: typing.Literal['set_var_object']
    var: str
    value: objects.Objects


class SetVarNumber(EffectModel):
    """Define a scripting variables to the given integer."""
    name: typing.Literal['set_var_number']
    var: str
    value: int


class SetVarLocation(EffectModel):
    """Define a scripting variables to the given Location."""
    name: typing.Literal['set_var_location']
    var: str
    value: locations.Location


class MoveUnit(EffectModel):
    """Changes the unit's location to the target square"""
    name: typing.Literal['move_unit']
    unit: objects.Unit
    location: locations.Location


class DealDamage(EffectModel):
    """Deals damage to the given unit."""
    name: typing.Literal['deal_damage']
    amount: properties.Number
    source: objects.Object = objects.this
    target: objects.Unit


# An effect cannot have a duration, such as killing a minion.
InstantaneousEffect = Union[DrawCards,
                            SetVarObject,
                            SetVarNumber,
                            SetVarLocation,
                            MoveUnit,
                            DealDamage]


class DurationEffectModel(EffectModel):  # model in the name indicates it's abstract.
    """An continuous effect."""
    until: typing.Optional[events.Event] = None


class ChangeProperty(DurationEffectModel):
    """Modify a property of an object."""
    name: typing.Literal['change_property']
    property_owner: objects.Objects = "this"
    property: properties.Property  # todo Only allow properties property_owner has? Or just ignore?
    operator: operators.NumberOperator = operators.plus
    by_value: properties.Number


# IF YOU USE THE abilities MODULE YOU MUST update_forward_refs() UNDER THE abilities IMPORT.

class AddAbility(DurationEffectModel):
    name: typing.Literal['add_ability']
    to: objects.Objects = objects.this
    ability: abilities.Ability


DurationEffect = Union[ChangeProperty, AddAbility]
Effect = Union[InstantaneousEffect, DurationEffect]

import abilities

AddAbility.update_forward_refs()
