import allure

from clients.episode.episode_client import EpisodeClient
from clients.episode.episode_schema import GetEpisodeResponseSchema
from tools.assertions.base_assertions import get_request, assert_equal


@allure.step("Check that episode id in response the same id in request")
def check_episode_id_response(response: int, episode_id: int):
    assert_equal(response, episode_id, "id")


@allure.step("Check that urls in response work")
def check_urls_episode(list_ids: GetEpisodeResponseSchema, client: EpisodeClient):
    get_request(list_ids.url, client)
    for j in list_ids.characters:
        get_request(j, client)
