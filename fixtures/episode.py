from clients.episode.episode_client import get_episode_client, EpisodeClient
from tools.fakers import fake
import pytest




@pytest.fixture
def episode_client() -> EpisodeClient:
    return get_episode_client()

@pytest.fixture
def random_episode_id() -> int:
    return fake.character_random_id()

@pytest.fixture
def non_existent_episode_id() -> int:
    return fake.non_exist_character_id()