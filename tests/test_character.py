from http import HTTPStatus

import allure
import pytest
from clients.character.character_schema import GetAllCharactersResponseSchema, GetCharacterResponseSchema, \
    GetMultipleCharactersResponseSchema, QueryParamsGetAllCharactersRequestSchema
from clients.errors_schemas import NotFoundErrorSchema
from constants.error_constants import Errors
from tools.allure.tags import AllureTag
from tools.assertions.base_assertions import assertion_status_code, check_not_found, check_ids_multiple, \
    check_query_in_response, check_unique_id
from tools.assertions.character_assertion import check_correct_status, check_correct_genders, \
    check_urls, check_char_id_response

@pytest.mark.regression
@allure.tag(AllureTag.CHARACTERS, AllureTag.REGRESSION)
class TestCharacter:
    @allure.tag(AllureTag.GET_ENTITIES)
    @allure.title("Get all characters")
    def test_get_all_characters(self, character_client):
        response = character_client.get_all_characters()
        response_data = GetAllCharactersResponseSchema.model_validate_json(response.text)

        assertion_status_code(response.status_code, HTTPStatus.OK)
        check_correct_genders(response_data)
        check_unique_id(response_data)
        check_correct_status(response_data)


    @allure.tag(AllureTag.GET_ENTITIES)
    @allure.title("Get characters by params")
    @pytest.mark.parametrize("query_params", [
    {"name": "Rick"},
    {"status": "Alive"},
    {"species": "Human"},
    {"type": "Genetic experiment"},
    {"gender": "Male"},
    {"name": "Rick", "status": "Alive"},
    {"name": "Abradolf Lincler", "status": "unknown", "species": "Human", "type": "Genetic experiment",
     "gender": "Male"},
])
    def test_get_all_characters_with_params(self, character_client, query_params):
        query = QueryParamsGetAllCharactersRequestSchema(**query_params)
        response = character_client.get_all_characters(query)
        response_data = GetAllCharactersResponseSchema.model_validate_json(response.text)

        assertion_status_code(response.status_code, HTTPStatus.OK)
        check_query_in_response(query, response_data)


    @allure.tag(AllureTag.GET_ENTITY)
    @allure.title("Get one character")
    def test_get_single_character(self, character_client, random_char_id):
        response = character_client.get_one_character(random_char_id)
        response_data = GetCharacterResponseSchema.model_validate_json(response.text)

        assertion_status_code(response.status_code, HTTPStatus.OK)
        check_char_id_response(response_data.id, random_char_id)
        check_urls(response_data, character_client)


    @allure.tag(AllureTag.GET_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.title("Trying get non-existent character")
    def test_negative_get_single_character(self, character_client, non_existent_char_id):
        response = character_client.get_one_character(non_existent_char_id)
        response_data = NotFoundErrorSchema.model_validate_json(response.text)

        assertion_status_code(response.status_code, HTTPStatus.NOT_FOUND)
        check_not_found(response_data, Errors.CHARACTER_ERROR_MSG)


    @allure.tag(AllureTag.GET_ENTITIES)
    @allure.title("Get several characters with list or tuple")
    @pytest.mark.parametrize("ids", [[1,2,3], (1,2,3)])
    def test_get_multiple_characters(self, character_client, ids):
        response = character_client.get_multiple_characters(ids)
        response_data = GetMultipleCharactersResponseSchema.model_validate_json(response.text)

        assertion_status_code(response.status_code, HTTPStatus.OK)
        check_ids_multiple(response_data, ids)


    @allure.tag(AllureTag.GET_ENTITIES, AllureTag.NEGATIVE_TEST)
    @allure.title("Trying get characters by params with incorrect value")
    @pytest.mark.parametrize("query_params", [
    {"name": "Non-Existent"},
    {"status": "Non-Existent"},
    {"species": "Non-Existent"},
    {"type": "Non-Existent"},
    {"gender": "Non-Existent"},
    {"name": "Non-Existent", "status": "Non-Existent"},
    {"name": "Non-Existent", "status": "Non-Existent", "species": "Non-Existent", "type": "Non-Existent",
     "gender": "Non-Existent"},
])
    def test_get_all_characters_with_wrong_params(self, character_client, query_params):
        query = QueryParamsGetAllCharactersRequestSchema(**query_params)
        response = character_client.get_all_characters(query)
        response_data = NotFoundErrorSchema.model_validate_json(response.text)

        assertion_status_code(response.status_code, HTTPStatus.NOT_FOUND)
        check_not_found(response_data, Errors.WRONG_PARAMS_MSG)