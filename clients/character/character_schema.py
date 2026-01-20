from datetime import datetime

from pydantic import BaseModel, HttpUrl, RootModel, Field


class Info(BaseModel):
    count: int
    pages: int
    next: HttpUrl | None=None
    prev: HttpUrl | None=None

class Origin(BaseModel):
    name: str
    url: str

class Location(BaseModel):
    name: str
    url: str

class GetCharacterResponseSchema(BaseModel):
    """
    Структура ответа на запрос одного персонажа
    """
    id: int
    name: str
    status: str
    species: str
    type: str
    gender: str
    origin: Origin
    location: Location
    image: HttpUrl
    episode: list[HttpUrl]
    url: HttpUrl
    created: datetime


class GetAllCharactersResponseSchema(BaseModel):
    """
    Структура ответа на запрос всех персонажей
    """
    info: Info
    results: list[GetCharacterResponseSchema]

class GetMultipleCharactersResponseSchema(RootModel):
    """
    Структура ответа на запрос нескольких персонажей
    """
    root: list[GetCharacterResponseSchema]


class QueryParamsGetAllCharactersRequestSchema(BaseModel):
    """
    Структура запроса с query параметрами на получение всех персонажей
    """
    name: str | None = None
    status: str | None = None
    species: str | None = None
    type: str | None = None
    gender: str | None = None
