import glob
import os

import pydantic
import typing

import models.cards
import models.decks

RESOURCES_DIR = 'resources'
CARDS_DIR = f'{RESOURCES_DIR}/cards'
DECKS_DIR = f'{RESOURCES_DIR}/decks'


def get_card(card_id: str) -> models.cards.CARD:
    return _get_resource(card_id, CARDS_DIR, models.cards.CARD)


def get_master_deck(deck_id: str) -> models.decks.MasterDeck:
    master_deck = _get_resource(deck_id, DECKS_DIR, models.decks.MasterDeck)
    return master_deck


ResourceType = typing.TypeVar('ResourceType')


def _get_resource(resource_id: str, base_dir: str, resource_type: typing.Type[ResourceType]) -> ResourceType:
    _set_wd()
    file_names = glob.glob(f'{base_dir}/**/{resource_id}.json', recursive=True)
    if not file_names:
        raise FileNotFoundError(f'No file matching {resource_id}.json in {base_dir}')
    if len(file_names) > 1:
        raise FileExistsError(f'Multiple files matching {resource_id} in {base_dir}: {file_names}')
    file_name = file_names[0]
    resource = pydantic.parse_file_as(resource_type, file_name)
    return resource


def _set_wd():
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
