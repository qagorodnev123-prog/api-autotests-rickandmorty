from httpx import Client

from clients.event_hooks import curl_event_hook
from config import settings


def get_http_client() -> Client:
    """
    Функция создает экземпляр httpx.Client с базовыми настройками.
    :return: Готовый к использованию объект httpx.Client
    """
    return Client(base_url=settings.http_client.client_url,
                  timeout=settings.http_client.timeout,
                  event_hooks={"request": [curl_event_hook]})