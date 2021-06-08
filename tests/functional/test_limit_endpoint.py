from http import HTTPStatus

from freezegun import freeze_time
from starlette.testclient import TestClient

from tests.fixtures import Fixtures

fixtures = Fixtures()


def setup_function():
    fixtures.clean_database()


def test_limit_requires_api_key(http_client: TestClient):
    headers = {}

    response = http_client.request("GET", "/limit", headers=headers)
    assert response.status_code == HTTPStatus.FORBIDDEN


@freeze_time('2021-06-12 00:00:01')
def test_limit_successful_if_count_lower_than_10(http_client: TestClient):
    fixtures.there_is_an_user_with_an_api_key_and_n_usage_at('foo', 'apikey', 9, '2021-06-12 00:00:01')
    api_key = 'apikey'
    headers = {'X-API-KEY': api_key}

    response = http_client.get("/limit", headers=headers)

    assert response.status_code == HTTPStatus.OK


@freeze_time('2021-06-12 00:00:01')
def test_limit_forbidden_if_count_greater_than_10(http_client: TestClient):
    fixtures.there_is_an_user_with_an_api_key_and_n_usage_at('foo', 'apikey', 10, '2021-06-12 00:00:01')
    api_key = 'apikey'
    headers = {'X-API-KEY': api_key}

    response = http_client.get("/limit", headers=headers)

    assert response.status_code == HTTPStatus.FORBIDDEN
