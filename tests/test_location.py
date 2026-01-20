from http import HTTPStatus

import allure
import pytest
from clients.errors_schemas import NotFoundErrorSchema
from clients.locations.location_schema import GetAllLocationsResponseSchema, QueryParamsGetAllLocationsRequestSchema, \
    GetLocationResponseSchema, GetMultipleLocationsResponseSchema
from constants.error_constants import Errors
from fixtures.location import location_client
from tools.allure.tags import AllureTag
from tools.assertions.base_assertions import assertion_status_code, check_not_found, check_ids_multiple, \
    check_query_in_response, check_unique_id
from tools.assertions.location_assertion import check_location_id_response, check_urls_locations

@pytest.mark.regression
@allure.tag(AllureTag.LOCATIONS, AllureTag.REGRESSION)
class TestLocation:
    @allure.tag(AllureTag.GET_ENTITIES)
    @allure.title("Get all locations")
    def test_get_all_locations(self, location_client):
        response = location_client.get_all_locations()
        response_data = GetAllLocationsResponseSchema.model_validate_json(response.text)

        assertion_status_code(response.status_code, HTTPStatus.OK)
        check_unique_id(response_data)


    @allure.tag(AllureTag.GET_ENTITIES)
    @allure.title("Get locations by params")
    @pytest.mark.parametrize("query_params", [
    {"name": "Earth"},
    {"type": "Planet"},
    {"dimension": "Replacement Dimension"},
    {"name": "Purge Planet", "type": "Planet", "dimension": "Replacement Dimension"},
])
    def test_get_all_locations_with_params(self, location_client, query_params):
        query = QueryParamsGetAllLocationsRequestSchema(**query_params)
        response = location_client.get_all_locations(query)
        response_data = GetAllLocationsResponseSchema.model_validate_json(response.text)

        assertion_status_code(response.status_code, HTTPStatus.OK)
        check_query_in_response(query, response_data)


    @allure.tag(AllureTag.GET_ENTITY)
    @allure.title("Get one location")
    def test_get_single_location(self, location_client, random_location_id):
        response = location_client.get_one_location(random_location_id)
        response_data = GetLocationResponseSchema.model_validate_json(response.text)

        assertion_status_code(response.status_code, HTTPStatus.OK)
        check_location_id_response(response_data.id, random_location_id)
        check_urls_locations(response_data, location_client)


    @allure.tag(AllureTag.GET_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.title("Trying get non-existent location")
    def test_negative_get_single_location(self, location_client, non_existent_location_id):
        response = location_client.get_one_location(non_existent_location_id)
        response_data = NotFoundErrorSchema.model_validate_json(response.text)

        assertion_status_code(response.status_code, HTTPStatus.NOT_FOUND)
        check_not_found(response_data, Errors.LOCATION_ERROR_MSG)


    @allure.tag(AllureTag.GET_ENTITIES)
    @allure.title("Get several locations with list or tuple")
    @pytest.mark.parametrize("ids", [[1,2,3], (1,2,3)])
    def test_get_multiple_locations(self, location_client, ids):
        response = location_client.get_multiple_locations(ids)
        response_data = GetMultipleLocationsResponseSchema.model_validate_json(response.text)

        assertion_status_code(response.status_code, HTTPStatus.OK)
        check_ids_multiple(response_data, ids)


    @allure.tag(AllureTag.GET_ENTITIES, AllureTag.NEGATIVE_TEST)
    @allure.title("Trying get locations by params with incorrect value")
    @pytest.mark.parametrize("query_params", [
    {"name": "Non-Existent"},
    {"type": "Non-Existent"},
    {"dimension": "Non-Existent"},
    {"name": "Non-Existent", "type": "Non-Existent", "dimension": "Non-Existent"},
])
    def test_get_all_locations_with_wrong_params(self, location_client, query_params):
        query = QueryParamsGetAllLocationsRequestSchema(**query_params)
        response = location_client.get_all_locations(query)
        response_data = NotFoundErrorSchema.model_validate_json(response.text)

        assertion_status_code(response.status_code, HTTPStatus.NOT_FOUND)
        check_not_found(response_data, Errors.WRONG_PARAMS_MSG)