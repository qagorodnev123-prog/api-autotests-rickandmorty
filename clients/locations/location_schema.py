from datetime import datetime

from pydantic import BaseModel, HttpUrl, RootModel, Field


class Info(BaseModel):
    count: int
    pages: int
    next: HttpUrl | None=None
    prev: HttpUrl | None=None


class GetLocationResponseSchema(BaseModel):
    """
    Структура ответа на запрос одной локации
    """
    id: int
    name: str
    type: str
    dimension: str
    residents: list
    url: HttpUrl
    created: datetime


class GetAllLocationsResponseSchema(BaseModel):
    """
    Структура ответа на запрос всех локаций
    """
    info: Info
    results: list[GetLocationResponseSchema]

class GetMultipleLocationsResponseSchema(RootModel):
    """
    Структура ответа на запрос нескольких локаций
    """
    root: list[GetLocationResponseSchema]

class QueryParamsGetAllLocationsRequestSchema(BaseModel):
    """
    Структура запроса с query параметрами на получение всех локаций
    """
    name: str | None = None
    type: str | None = None
    dimension: str | None = None