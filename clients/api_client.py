from httpx import Client, QueryParams, Response, URL
import allure

class APIClient:
    def __init__(self, client: Client):
        """
        Базовый API клиент, принимающий объект httpx.Client.

        :param client: экземпляр httpx.Client для выполнения HTTP-запросов
        """
        self.client = client

    @allure.step("Make GET request to {url}")
    def get(self, url: URL | str, params: QueryParams | None=None) -> Response:
        """
        Выполняет GET запрос
        :param url:
        :param params:
        :return:
        """
        return self.client.get(url, params=params)
