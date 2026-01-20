import allure

from clients.locations.location_client import LocationClient
from clients.locations.location_schema import GetLocationResponseSchema
from tools.assertions.base_assertions import get_request, assert_equal


@allure.step("Check that location id in response the same id in request")
def check_location_id_response(response: int, location_id: int):
    assert_equal(response, location_id, "id")


@allure.step("Check that urls in response work")
def check_urls_locations(list_ids: GetLocationResponseSchema, client: LocationClient):
    get_request(list_ids.url, client)
    for j in list_ids.residents:
        get_request(j, client)

