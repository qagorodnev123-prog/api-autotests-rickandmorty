from httpx import Client

from clients.event_hooks import curl_event_hook


def get_http_client() -> Client:
    """
    Функция создает экземпляр httpx.Client с базовыми настройками.
    :return: Готовый к использованию объект httpx.Client
    """
    return Client(base_url='https://rickandmortyapi.com/api',
                  timeout=100,
                  event_hooks={"request": [curl_event_hook]})