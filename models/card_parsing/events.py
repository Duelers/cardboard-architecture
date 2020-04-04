from __future__ import annotations

from typing import Union, Literal

import typing

import base
import comparison

import objects
import players

summon = 'summon'  # Opening gambit. When this is played.
death = 'death' # Dying wish

class EndOfNTurnsFromNow(base.BaseModel):
    name: typing.Literal['end_of_#_turns_from_now']
    num_turns: int = 0


class StartOfTurn(base.BaseModel):
    name: typing.Literal['start_of_turn']
    turn_owner: typing.Optional[players.Player] = None


class EndOfTurn(base.BaseModel):
    name: typing.Literal['end_of_turn']
    turn_owner: typing.Optional[players.Player] = None


class SpellCast(base.BaseModel):
    name: typing.Literal['spell_cast']
    target: typing.Optional[objects.Objects] = None
    caster: typing.Optional[players.Player] = None


class DamageDealt(base.BaseModel):
    name: typing.Literal['damage_dealt']
    attacker: typing.Optional[objects.Objects] = None
    target: typing.Optional[objects.Objects] = None
    minimum: typing.Optional[int] = None
    maximum: typing.Optional[int] = None


# Requires Event
class ConditionalTrigger(base.BaseModel):
    name: typing.Literal['conditional_trigger']
    trigger: Event
    conditions: typing.Union[comparison.Comparison,
                             typing.List[comparison.Comparison]
    ]


Event = Union[
    Literal[summon],
    Literal[death],
    EndOfNTurnsFromNow,
    StartOfTurn,
    EndOfTurn,
    SpellCast,
    DamageDealt,
    ConditionalTrigger
]  # A thing that happens, such as a turn ending.

ConditionalTrigger.update_forward_refs()
