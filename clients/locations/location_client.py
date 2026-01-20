from httpx import Response

from clients.api_client import APIClient
from clients.http_builder import get_http_client
from clients.locations.location_schema import QueryParamsGetAllLocationsRequestSchema


class LocationClient(APIClient):

    def get_all_locations(self, query: QueryParamsGetAllLocationsRequestSchema | None = None) -> Response:
        """
        Метод получения всех локаций
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        if query is not None:
            return self.get(f'location', params=query.model_dump(by_alias=True))
        else:
            return self.get(f'location')

    def get_one_location(self, location_id: int) -> Response:
        """
        Метод получения одной локации

        :param location_id: id локации
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.get(f'location/{location_id}')


    def get_multiple_locations(self, *ids) -> Response:
        """
        Принимает ID локаций в виде:
        get_locations(1, 2, 3)
        get_locations([1, 2, 3])
        """
        if len(ids) == 1 and isinstance(ids[0], (list, tuple)):
            location_ids = ids[0]
        else:
            location_ids = ids
        str_ids = ",".join(map(str, location_ids))

        return self.get(f"location/{str_ids}")

def get_location_client() -> LocationClient:
    return LocationClient(client=get_http_client())