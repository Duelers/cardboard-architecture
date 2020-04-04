import typing
import models.cards
import models.decks
from . import networking_to_view


class Model:
    """A wrapper for GameState that provides an interface for updating it."""

    def __init__(self, my_deck: models.decks.Deck):
        self._game_state: models.GameState = models.GameState.new_game(my_deck)
        self._effect_log: typing.List[models.BaseEffect] = []

    @property
    def game_state(self):
        return self._game_state

    def update(self, update: models.GameUpdate) -> typing.NoReturn:
        self._game_state = update.game_state

        if update.effect:
            self._effect_log.append(update.effect)

        networking_to_view.send_update(update)
