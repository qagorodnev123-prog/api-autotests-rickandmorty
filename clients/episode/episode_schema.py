from datetime import datetime

from pydantic import BaseModel, HttpUrl, RootModel, Field


class Info(BaseModel):
    count: int
    pages: int
    next: HttpUrl | None=None
    prev: HttpUrl | None=None


class GetEpisodeResponseSchema(BaseModel):
    """
    Структура ответа на запрос одного эпизода
    """
    id: int
    name: str
    air_date: str
    episode: str
    characters: list
    url: HttpUrl
    created: datetime


class GetAllEpisodesResponseSchema(BaseModel):
    """
    Структура ответа на запрос всех эпизодов
    """
    info: Info
    results: list[GetEpisodeResponseSchema]

class GetMultipleEpisodesResponseSchema(RootModel):
    """
    Структура ответа на запрос нескольких эпизодов
    """
    root: list[GetEpisodeResponseSchema]

class QueryParamsGetAllEpisodesRequestSchema(BaseModel):
    """
    Структура запроса с query параметрами на получение всех эпизодов
    """
    name: str | None = None
    episode: str | None = None