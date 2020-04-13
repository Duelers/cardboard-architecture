from __future__ import annotations

import typing

from . import card_types
from . import generals
from . import player_labels
from . import base
from . import zones

if typing.TYPE_CHECKING:
    import models

trigger = "trigger"  # The event which causes a triggered effect


class This(base.SingleGetter[object]):
    def get(self, game_state: models.GameState, this: models.cards.BaseCard):
        return this


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

    owner: typing.Optional[player_labels.Player] = None


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
    owner: typing.Optional[player_labels.Player] = None


# Choose unit
class UnitSelectionModel(base.BaseModel):
    types: typing.Union[
        card_types.CardType,
        typing.List[card_types.CardType]
    ] = card_types.minion

    owner: typing.Optional[player_labels.Player] = None
    from_cells: locations.MultipleLocation = "everywhere"  # todo this is terrible. Should be locations.everywhere but I
    # can't figure out how to import that without a circular dependency.


# class ChooseUnit(UnitSelectionModel):
#     name: typing.Literal['choose_unit']


class GetVarObject(base.BaseModel):
    name: typing.Literal['get_var_object']
    var: str


from . import object_types

# def make_choose_unit(object_type: object_types.ObjectType):
#     model = object_types.make_typed_model(object_type,
#                                           name='ChooseUnit',
#                                           owner=(typing.Optional[player_labels.Player], None),
#                                           from_cells=('locations.Locations', "everywhere")
#                                           )
#     model.__module__ = __name__
#     return model


# choose_minion = make_choose_unit(object_types.MinionType)

Minion = typing.Union[This,
                      ChooseCard,
                      # choose_minion,
                      GetVarObject]  # todo type

# choose_general = make_choose_unit(object_types.GeneralType)

General = typing.Union[generals.Generals,
                       This,
                       ChooseCard,
                       # choose_general,
                       GetVarObject]  # todo

# choose_unit = make_choose_unit(object_types.UnitType)

Unit = typing.Union[generals.Generals,
                    This,
                    ChooseCard,
                    # choose_unit,
                    GetVarObject]  # todo

Spell = typing.Union[This,
                     ChooseCard,
                     GetVarObject]  # todo

Artifact = typing.Union[This,
                        ChooseCard,
                        GetVarObject]  # todo

Units = typing.Union[Unit, ChooseCards]

Object = typing.Union[This,
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

from . import locations

#
# choose_unit.update_forward_refs()
# choose_general.update_forward_refs()
# choose_minion.update_forward_refs()

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
