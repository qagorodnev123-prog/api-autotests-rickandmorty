from tools.fakers import fake
import pytest

from clients.character.character_client import CharacterClient, get_character_client



@pytest.fixture
def character_client() -> CharacterClient:
    return get_character_client()

@pytest.fixture
def random_char_id() -> int:
    return fake.character_random_id()

@pytest.fixture
def non_existent_char_id() -> int:
    return fake.non_exist_character_id()
