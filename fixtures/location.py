from clients.locations.location_client import LocationClient, get_location_client
from tools.fakers import fake
import pytest




@pytest.fixture
def location_client() -> LocationClient:
    return get_location_client()

@pytest.fixture
def random_location_id() -> int:
    return fake.character_random_id()

@pytest.fixture
def non_existent_location_id() -> int:
    return fake.non_exist_character_id()