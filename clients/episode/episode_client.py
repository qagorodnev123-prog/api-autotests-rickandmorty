from httpx import Response

from clients.api_client import APIClient
from clients.episode.episode_schema import QueryParamsGetAllEpisodesRequestSchema
from clients.http_builder import get_http_client



class EpisodeClient(APIClient):

    def get_all_episodes(self, query: QueryParamsGetAllEpisodesRequestSchema | None = None) -> Response:
        """
        Метод получения всех эпизодов
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        if query is not None:
            return self.get(f'episode', params=query.model_dump(by_alias=True))
        else:
            return self.get(f'episode')

    def get_one_episode(self, episode_id: int) -> Response:
        """
        Метод получения одного эпизода

        :param episode_id: id эпизода
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.get(f'episode/{episode_id}')


    def get_multiple_episodes(self, *ids) -> Response:
        """
        Принимает ID эпизодов в виде:
        get_locations(1, 2, 3)
        get_locations([1, 2, 3])
        """
        if len(ids) == 1 and isinstance(ids[0], (list, tuple)):
            episode_id = ids[0]
        else:
            episode_id = ids
        str_ids = ",".join(map(str, episode_id))

        return self.get(f"episode/{str_ids}")

def get_episode_client() -> EpisodeClient:
    return EpisodeClient(client=get_http_client())