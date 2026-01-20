from httpx import Response

from clients.api_client import APIClient
from clients.character.character_schema import QueryParamsGetAllCharactersRequestSchema
from clients.http_builder import get_http_client


class CharacterClient(APIClient):

    def get_all_characters(self, query: QueryParamsGetAllCharactersRequestSchema | None = None) -> Response:
        """
        Метод получения всех персонажей
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        if query is not None:
            return self.get(f'character', params=query.model_dump(by_alias=True))
        else:
            return self.get(f'character')

    def get_one_character(self, character_id: int) -> Response:
        """
        Метод получения одного персонажа

        :param character_id: id персонажа
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.get(f'character/{character_id}')


    def get_multiple_characters(self, *ids) -> Response:
        """
        Принимает ID персонажей в виде:
        get_characters(1, 2, 3)
        get_characters([1, 2, 3])
        """
        if len(ids) == 1 and isinstance(ids[0], (list, tuple)):
            character_ids = ids[0]
        else:
            character_ids = ids
        str_ids = ",".join(map(str, character_ids))

        return self.get(f"character/{str_ids}")

def get_character_client() -> CharacterClient:
    return CharacterClient(client=get_http_client())
