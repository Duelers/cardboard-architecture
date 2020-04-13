import typing
import models.cards
import models.decks
from . import networking_to_view
from . import new_game_constructor


class Model:
    """A wrapper for GameState that provides an interface for updating it."""

    def __init__(self, master_decks: typing.Tuple[models.decks.MasterDeck, models.decks.MasterDeck]):
        self._game_state = new_game_constructor.generate_new_game(master_decks)

        self._effect_log: typing.List[models.BaseEffect] = []

    @property
    def game_state(self):
        return self._game_state

    def update(self, update: models.GameUpdate) -> typing.NoReturn:
        self._game_state = update.game_state

        if update.effect:
            self._effect_log.append(update.effect)

        networking_to_view.send_update(update)
