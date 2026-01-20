from http import HTTPStatus
from typing import Any
from collections import Counter

import allure


@allure.step("Check that response status code equals to {expected}")
def assertion_status_code(actual: int, expected: int):
    assert actual == expected, (
        f"Incorrect status",
        f"Expected status-code: {expected}"
        f"Actual status-code: {actual}"
    )


@allure.step("Check that {name} equals to {expected}")
def assert_equal(actual: Any, expected: Any, name: str):
    assert actual == expected, (
        f"Incorrect value: {name}"
        f"Actual value: {actual}"
        f"Expected value: {expected}"
    )


@allure.step("Check that sending request on {url} is possible")
def get_request(url, client):
    response = client.get(str(url))
    assert response.status_code == HTTPStatus.OK, (
        f"URL {url} недоступен. Статус код: {response.status_code}")


@allure.step("Check getting an error 404")
def check_not_found(response: Any, error_msg: str):
    assert_equal(response.error, error_msg, "error")


@allure.step("Check ids in response and request")
def check_ids_multiple(response: Any, ids: Any):
    if isinstance(ids, (list, tuple)):
        ids = list(ids)
    else:
        ids = [ids]
    assert len(response.root) == len(ids), (
            f"Количество ID в ответе ({len(response.root)}) "
            f"не соответствует количеству запрошенных ID ({len(ids)})"
    )
    response_ids = [item.id for item in response.root]
    for i in range(len(ids)):
        assert_equal(ids[i], response_ids[i], "id")


@allure.step("Check that we get entities by filters")
def check_query_in_response(query: Any, response: Any):
    query_dict = query.model_dump(exclude_none=True)
    for k,v in query_dict.items():
        for i in response.results:
            actual_value = getattr(i,k)
            assert v in actual_value, (
                    f"Фильтр '{k}'"
                    f"Полученное значение '{actual_value}', "
                    f"ожидалось '{v}'"
            )


@allure.step("Check that every id is unique")
def check_unique_id(list_ids: Any):
    ids = [i.id for i in list_ids.results]
    counts = Counter(ids)
    duplicates = [item for item, count in counts.items() if count > 1]
    assert not duplicates, f"Найдены дубликаты ID в ответе: {duplicates}"