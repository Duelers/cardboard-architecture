from __future__ import annotations

import typing

import card_types
import generals
import players
import base

import zones

this = "this"
trigger = "trigger"  # The event which causes a triggered effect


class CardSelectionModel(base.BaseModel):
    """Selects cards from out-of-play zones, such as a player's hand."""
    from_zones: typing.Union[
        zones.CardZone,
        typing.List[zones.CardZone]
    ] = zones.hand

    types: typing.Union[
        card_types.CardType,
        typing.List[card_types.CardType]
    ]

    owner: typing.Optional[players.Player] = None


class ChooseCard(CardSelectionModel):
    name: typing.Literal['choose_card']


class ChooseCards(CardSelectionModel):
    name: typing.Literal['choose_cards']
    choose_at_least: typing.Optional[int] = 1
    choose_at_most: typing.Optional[int] = 1


class AllCards(CardSelectionModel):
    name: typing.Literal['all_cards']
    from_zones: typing.Union[
        zones.CardZone,
        typing.List[zones.CardZone]
    ] = zones.in_play
    types: typing.Union[
        card_types.CardType,
        typing.List[card_types.CardType]
    ]
    owner: typing.Optional[players.Player] = None


# Choose unit

class UnitSelectionModel(base.BaseModel):
    types: typing.Union[
        card_types.CardType,
        typing.List[card_types.CardType]
    ] = card_types.minion

    owner: typing.Optional[players.Player] = None
    from_cells: locations.Locations = "everywhere"  # todo this is terrible. Should be locations.everywhere but I
    # can't figure out how to import that without a circular dependency.


# class ChooseUnit(UnitSelectionModel):
#     name: typing.Literal['choose_unit']


class GetVarObject(base.BaseModel):
    name: typing.Literal['get_var_object']
    var: str


import object_types


def make_choose_unit(object_type: object_types.ObjectType):
    # noinspection PyTypeChecker
    model = object_types.make_typed_model(object_type,
                                          name='ChooseUnit',
                                          owner=(typing.Optional[players.Player], None),
                                          from_cells=('locations.Locations', "everywhere")
                                          )
    model.__module__ = __name__
    return model


choose_minion = make_choose_unit(object_types.MinionType)

Minion = typing.Union[typing.Literal[this],
                      ChooseCard,
                      choose_minion,
                      GetVarObject]  # todo type

choose_general = make_choose_unit(object_types.GeneralType)

General = typing.Union[generals.Generals,
                       typing.Literal[this],
                       ChooseCard,
                       choose_general,
                       GetVarObject]  # todo

choose_unit = make_choose_unit(object_types.UnitType)

Unit = typing.Union[generals.Generals,
                    typing.Literal[this],
                    ChooseCard,
                    choose_unit,
                    GetVarObject]  # todo

Spell = typing.Union[typing.Literal[this],
                     ChooseCard,
                     GetVarObject]  # todo

Artifact = typing.Union[typing.Literal[this],
                        ChooseCard,
                        GetVarObject]  # todo

Units = typing.Union[Unit, ChooseCards]

Object = typing.Union[typing.Literal[this],
                      typing.Literal[trigger],
                      Minion,
                      General,
                      Spell,
                      Artifact,
                      ChooseCard,
                      GetVarObject]

Objects = typing.Union[
    Object,
    ChooseCards,
    AllCards,
]

import locations

choose_unit.update_forward_refs()
choose_general.update_forward_refs()
choose_minion.update_forward_refs()

# clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)
# print(clsmembers)


object_key = 'object'
object_types.UnitType[object_key] = Unit
object_types.MinionType[object_key] = Minion
object_types.GeneralType[object_key] = General
object_types.SpellType[object_key] = Spell
object_types.ArtifactType[object_key] = Artifact
#
# objects_key = 'objects'
# UnitType[objects_key] = objects.Units
# MinionType[objects_key] = objects.Minions
# GeneralType[objects_key] = objects.Generals
# SpellType[objects_key] = objects.Spells
# ArtifactType[objects_key] = objects.Artifacts
#
