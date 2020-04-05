from . import load_resources
import models.decks


def generate_new_game(
        my_master_deck: models.decks.MasterDeck):  # Todo, later this should take two players, instead of a deck.
    """Constructor for default initial game state."""

    listener = models.Listener(trigger_effect_type='MoveEffect',
                               response_actions=[
                                   models.ChangeSomeValueAction(increase_by=1)
                               ])

    my_general = master_deck_to_general(my_master_deck)
    my_current_deck = master_deck_to_current_deck(my_master_deck)

    board = [[None, None, my_general, None, None],
             [None, None, None, None, None],
             [None, None, None, None, None],
             [None, None, None, None, None],
             [None, None, None, None, None],
             [None, None, None, None, None],
             [None, None, None, None, None]]

    player_1_state = models.PlayerState(deck=my_current_deck)

    new_game_state = models.GameState(board=board,
                                      some_value=0,
                                      listeners=[listener],
                                      player_1_state=player_1_state)

    return new_game_state


def master_deck_to_general(master_deck: models.decks.MasterDeck) -> models.cards.General:
    general = load_resources.get_card(master_deck.general_id)
    return general


def master_deck_to_current_deck(master_deck: models.decks.MasterDeck):
    cards = []
    for card_inclusion in master_deck.cards:
        card = load_resources.get_card(card_inclusion.card_id)
        cards += [card] * card_inclusion.count
    current_deck = models.decks.CurrentDeck(cards=cards)
    return current_deck
