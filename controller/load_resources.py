import glob
import os

import typing
import importlib.util

import models.cards
import models.decks
import models.players

RESOURCES_DIR = 'resources'
CARDS_DIR = f'{RESOURCES_DIR}/cards'
DECKS_DIR = f'{RESOURCES_DIR}/decks'


def get_card(card_id: str, player_number: models.players.PlayerNumber) -> models.cards.BaseCard:
    card: models.cards.BaseCard = _get_resource(card_id, CARDS_DIR, models.cards.BaseCard)
    card.player = player_number
    return card


def get_master_deck(deck_id: str) -> models.decks.MasterDeck:
    master_deck = _get_resource(deck_id, DECKS_DIR, models.decks.MasterDeck)
    return master_deck


ResourceType = typing.TypeVar('ResourceType')


def _get_resource(resource_id: str, base_dir: str, resource_type: typing.Type[ResourceType]) -> ResourceType:
    _set_wd()
    file_names = glob.glob(f'{base_dir}/**/{resource_id}.py', recursive=True)
    if not file_names:
        raise FileNotFoundError(f'No file matching {resource_id}.py in {base_dir}')
    if len(file_names) > 1:
        raise FileExistsError(f'Multiple files matching {resource_id} in {base_dir}: {file_names}')
    file_name = file_names[0]

    spec = importlib.util.spec_from_file_location("module.name", file_name)
    resource_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(resource_module)

    try:
        resource = resource_module.resource
        return resource
    except ValueError:  # todo fix error type
        raise ValueError(f'Resource file {file_name} does not create a resource attribute.')


def _set_wd():
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
