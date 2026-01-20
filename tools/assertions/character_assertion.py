import allure

from clients.character.character_client import CharacterClient
from clients.character.character_schema import GetAllCharactersResponseSchema, GetCharacterResponseSchema
from constants.character_constatns import Genders, Status
from tools.assertions.base_assertions import get_request, assert_equal


@allure.step("Check that gender is correct")
def check_correct_genders(list_ids: GetAllCharactersResponseSchema):
    for g in list_ids.results:
        gender = g.gender.lower()
        assert gender in Genders, (
            f"Incorrect gender: {g.gender}"
            f"Gender should be one of these: {Genders}"
        )


@allure.step("Check that status is correct")
def check_correct_status(list_ids: GetAllCharactersResponseSchema):
    for s in list_ids.results:
        status_life = s.status.lower()
        assert status_life in Status, (
            f"Incorrect status: {status_life}"
            f"Status should be one of these: {Status}"
        )


@allure.step("Check that urls in response work")
def check_urls(list_ids: GetCharacterResponseSchema, client: CharacterClient):
    location_url = list_ids.location.url
    origin_url = list_ids.origin.url
    if location_url:
        get_request(location_url, client)
    if origin_url:
        get_request(origin_url, client)
    get_request(list_ids.image, client)
    get_request(list_ids.url, client)
    for j in list_ids.episode:
        get_request(j, client)


@allure.step("Check that character id in response the same id in request")
def check_char_id_response(response: int, character_id: int):
    assert_equal(response, character_id, "id")

