from __future__ import annotations

import typing

import events
import base

airdrop = 'airdrop'


class AbilityModel(base.BaseModel):
    description: str = None


# IF YOU USE THE effects MODULE YOU MUST update_forward_refs() UNDER THE effects IMPORT.
class TriggeredEffects(AbilityModel):
    name: typing.Literal['triggered_effects']
    trigger: events.Event
    effects: typing.Optional[
        typing.Union[
            effects.Effect,
            typing.List[effects.Effect]
        ]
    ] = None
    cancel: bool = False


class ContinuousEffect(AbilityModel):
    name: typing.Literal['continuous_effect']
    effect: effects.Effect


Ability = typing.Union[TriggeredEffects,
                       ContinuousEffect,
                       typing.Literal[airdrop]]

import effects

TriggeredEffects.update_forward_refs()
ContinuousEffect.update_forward_refs()
