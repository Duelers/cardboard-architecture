import controller.networking_to_view
import models.effects
import models.events
import models.game_update
from . import game_model


class GameLogic:
    def handle_effect(self, effect: models.effects.BaseEffect):
        event = effect.to_event(game_model.Model.get())
        return self.handle_event(event)

    def handle_event(self, event: models.events.BaseEvent):
        old_model = game_model.Model.get()
        new_model = event.update_model(old_model)
        update = models.game_update.GameUpdate(game_state=new_model, event=event)

        game_model.Model.update(update)  # todo, maybe this could be cleaner? Big side effect.

        return update


_logic = GameLogic()


def update_game_logic(effect: models.effects.BaseEffect):
    _logic.handle_effect(effect)
