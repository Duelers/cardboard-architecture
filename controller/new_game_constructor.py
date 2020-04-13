import typing

import models.zones
from . import load_resources
import models.decks


def generate_new_game(master_decks: typing.Tuple[models.decks.MasterDeck, models.decks.MasterDeck]):
    """Constructor for default initial game state."""

    card_registry = models.CardRegistry()
    location_registry = models.LocationRegistry()

    player_states = _generate_player_states(master_decks, card_registry, location_registry)

    # listener is test code
    listener = models.Listener(trigger_effect_type='MoveEffect',
                               response_actions=[models.ChangeSomeValueAction(increase_by=1)])
    new_game_state = models.GameState(listeners=[listener],
                                      player_1_state=player_states[0],
                                      player_2_state=player_states[1],
                                      card_registry=card_registry,
                                      location_registry=location_registry
                                      )

    generals = _generate_generals(master_decks, card_registry)

    for general, location in zip(generals, models.cells.GENERAL_LOCATIONS):
        _add_general(new_game_state, general, location)

    return new_game_state


def _master_deck_to_general(master_deck: models.decks.MasterDeck,
                            player_number: models.players.PlayerNumber,
                            card_registry: models.CardRegistry) -> models.cards.General:
    general = load_resources.get_card(master_deck.general_id, player_number)
    card_registry.register(general)
    return general


def _master_deck_to_current_deck(master_deck: models.decks.MasterDeck,
                                 card_registry: models.CardRegistry,
                                 player_number: models.players.PlayerNumber) -> models.decks.CurrentDeck:
    cards = []
    for card_inclusion in master_deck.cards:
        card = load_resources.get_card(card_inclusion.card_id, player_number)
        for i in range(card_inclusion.count):
            card = card.copy(deep=True)
            card_registry.register(card)
            cards.append(card)
    current_deck = models.decks.CurrentDeck(cards=cards)
    return current_deck


def _generate_generals(master_decks: typing.Tuple[models.decks.MasterDeck, models.decks.MasterDeck],
                       card_registry: models.CardRegistry):
    generals = []
    for player_number, master_deck in zip((1, 2), master_decks):
        general = _master_deck_to_general(master_decks[0], player_number, card_registry)
        generals.append(general)
    return tuple(generals)


def _generate_player_states(master_decks: typing.Tuple[models.decks.MasterDeck, models.decks.MasterDeck],
                            card_registry: models.CardRegistry,
                            location_registry: models.LocationRegistry):
    player_states = []
    for player_number, master_deck in zip((1, 2), master_decks):
        state = _generate_player_state(master_decks[0], player_number, card_registry, location_registry)
        player_states.append(state)
    return tuple(player_states)


def _generate_player_state(master_deck: models.decks.MasterDeck,
                           player_number: models.players.PlayerNumber,
                           card_registry: models.CardRegistry,
                           location_registry: models.LocationRegistry):
    current_deck = _master_deck_to_current_deck(master_deck, card_registry, player_number)
    for card in current_deck.cards:
        location_registry.register(
            card.instance_id, models.zones.PlayerZone(zone=models.zones.Deck, player=player_number)
        )
    player_1_state = models.PlayerState(deck=current_deck)
    return player_1_state


def _add_general(game_state: models.GameState,
                 general: models.cards.General,
                 board_location: models.cells.BoardLocation):
    game_state.board[board_location.x][board_location.y] = general
    game_state.location_registry.register(general.instance_id, board_location)
