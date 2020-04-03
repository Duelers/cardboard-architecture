import typing

import models
from . import game_model


class ModelUpdater:
    def __init__(self, model: game_model.Model):
        self.model = model

    def handle_action(self, action: models.BaseAction):
        event = action.to_event(self.model.game_state)
        return self.handle_event(event)

    def handle_event(self, event: models.BaseEvent):
        old_game_state = self.model.game_state
        self._listen_to_event(event, old_game_state.listeners)

        # Todo allow event modification. "When a spell would deal damage, it deals 1 more damage."
        new_game_state = event.update_model(old_game_state)
        update = models.GameUpdate(game_state=new_game_state, event=event)

        self.model.update(update)

        return update

    def _listen_to_event(self, event: models.BaseEvent, listeners: typing.List[models.Listener]):
        for listener in listeners:  # move to own function todo
            if listener.trigger_event_type == type(event).__name__:
                for response_action in listener.response_actions:
                    self.handle_action(response_action)
