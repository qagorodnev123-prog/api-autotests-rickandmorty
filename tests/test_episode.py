from http import HTTPStatus

import allure
import pytest

from clients.episode.episode_schema import GetAllEpisodesResponseSchema, QueryParamsGetAllEpisodesRequestSchema, \
    GetEpisodeResponseSchema, GetMultipleEpisodesResponseSchema
from clients.errors_schemas import NotFoundErrorSchema
from constants.error_constants import Errors
from fixtures.episode import episode_client
from tools.allure.tags import AllureTag
from tools.assertions.base_assertions import assertion_status_code, check_not_found, check_ids_multiple, \
    check_query_in_response, check_unique_id
from tools.assertions.episode_assertion import check_episode_id_response, check_urls_episode

@pytest.mark.regression
@allure.tag(AllureTag.EPISODES, AllureTag.REGRESSION)
class TestEpisode:
    @allure.tag(AllureTag.GET_ENTITIES)
    @allure.title("Get all episodes")
    def test_get_all_episodes(self, episode_client):
        response = episode_client.get_all_episodes()
        response_data = GetAllEpisodesResponseSchema.model_validate_json(response.text)

        assertion_status_code(response.status_code, HTTPStatus.OK)
        check_unique_id(response_data)


    @allure.tag(AllureTag.GET_ENTITIES)
    @allure.title("Get episodes by params")
    @pytest.mark.parametrize("query_params", [
    {"name": "Raising Gazorpazorp"},
    {"episode": "S01E09"},
    {"name": "Close Rick-counters of the Rick Kind", "episode": "S01E10"},
])
    def test_get_all_episodes_with_params(self, episode_client, query_params):
        query = QueryParamsGetAllEpisodesRequestSchema(**query_params)
        response = episode_client.get_all_episodes(query)
        response_data = GetAllEpisodesResponseSchema.model_validate_json(response.text)

        assertion_status_code(response.status_code, HTTPStatus.OK)
        check_query_in_response(query, response_data)


    @allure.tag(AllureTag.GET_ENTITY)
    @allure.title("Get one location")
    def test_get_single_episode(self, episode_client, random_episode_id):
        response = episode_client.get_one_episode(random_episode_id)
        response_data = GetEpisodeResponseSchema.model_validate_json(response.text)

        assertion_status_code(response.status_code, HTTPStatus.OK)
        check_episode_id_response(response_data.id, random_episode_id)
        check_urls_episode(response_data, episode_client)


    @allure.tag(AllureTag.GET_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.title("Trying get non-existent episode")
    def test_negative_get_single_episode(self, episode_client, non_existent_episode_id):
        response = episode_client.get_one_episode(non_existent_episode_id)
        response_data = NotFoundErrorSchema.model_validate_json(response.text)

        assertion_status_code(response.status_code, HTTPStatus.NOT_FOUND)
        check_not_found(response_data, Errors.EPISODE_ERROR_MSG)


    @allure.tag(AllureTag.GET_ENTITIES)
    @allure.title("Get several episodes with list or tuple")
    @pytest.mark.parametrize("ids", [[1,2,3], (1,2,3)])
    def test_get_multiple_episodes(self, episode_client, ids):
        response = episode_client.get_multiple_episodes(ids)
        response_data = GetMultipleEpisodesResponseSchema.model_validate_json(response.text)

        assertion_status_code(response.status_code, HTTPStatus.OK)
        check_ids_multiple(response_data, ids)


    @allure.tag(AllureTag.GET_ENTITIES, AllureTag.NEGATIVE_TEST)
    @allure.title("Trying get episodes by params with incorrect value")
    @pytest.mark.parametrize("query_params", [
    {"name": "Non-Existent"},
    {"episode": "Non-Existent"},
    {"name": "Non-Existent", "episode": "Non-Existent"},
])
    def test_get_all_episodes_with_wrong_params(self, episode_client, query_params):
        query = QueryParamsGetAllEpisodesRequestSchema(**query_params)
        response = episode_client.get_all_episodes(query)
        response_data = NotFoundErrorSchema.model_validate_json(response.text)

        assertion_status_code(response.status_code, HTTPStatus.NOT_FOUND)
        check_not_found(response_data, Errors.WRONG_PARAMS_MSG)