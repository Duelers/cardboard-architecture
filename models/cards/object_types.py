import dataclasses
import typing

import inflection
import pydantic


@dataclasses.dataclass
class ObjectType:
    type: str
    object: typing.Type
    property: typing.Type


type_key = 'type'
UnitType = {type_key: 'unit'}
MinionType = {type_key: 'minion'}
GeneralType = {type_key: 'general'}
SpellType = {type_key: 'spell'}
ArtifactType = {type_key: 'artifact'}

# UnitType = ObjectType(type='unit',
#                       object=objects.Unit,
#                       property=properties.UnitProperty)
#
# MinionType = ObjectType(type='minion',
#                         object=objects.Minion,
#                         property=properties.MinionProperty)
#
# GeneralType = ObjectType(type='general',
#                          object=objects.General,
#                          property=properties.GeneralProperty)
#
# SpellType = ObjectType(type='spell',
#                        object=objects.Spell,
#                        property=properties.SpellProperty)
#
# ArtifactType = ObjectType(type='artifact',
#                           object=objects.Artifact,
#                           property=properties.ArtifactProperty)

"""
any
    unit
        minion
        general
    spell
    artifact
    ability
    effect
    event


"""


def make_typed_model(obj_type: dict, name: str, **keys) -> typing.Type[pydantic.BaseModel]:
    snake_name = inflection.underscore(name)
    model = pydantic.create_model(
        model_name=f'{name}_{obj_type[type_key]}',
        name=(typing.Literal[snake_name], ...),
        type=(typing.Literal[obj_type[type_key]], obj_type[type_key]),
        **keys,
    )
    return model
