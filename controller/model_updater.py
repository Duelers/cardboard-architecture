import typing

import models
from . import game_model


class ModelUpdater:
    def __init__(self, model: game_model.Model):
        self.model = model

    def handle_action(self, action: models.BaseAction):
        effect = action.to_effect(self.model.game_state)
        return self.handle_effect(effect)

    def handle_effect(self, effect: models.BaseEffect):
        old_game_state = self.model.game_state
        self._all_listen_to_effect(effect, old_game_state.listeners)

        # Todo allow effect modification. "When a spell would deal damage, it deals 1 more damage."
        new_game_state = effect.update_model(old_game_state)
        update = models.GameUpdate(game_state=new_game_state, effect=effect)

        self.model.update(update)

        return update

    def _all_listen_to_effect(self, effect: models.BaseEffect, listeners: typing.List[models.Listener]):
        for listener in listeners:
            self._listen_to_effect(effect, listener)

    def _listen_to_effect(self, effect: models.BaseEffect, listener: models.Listener):
        if listener.trigger_effect_type == type(effect).__name__:
            for response_action in listener.response_actions:
                self.handle_action(response_action)
