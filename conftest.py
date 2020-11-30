import pytest
import requests
import json


def pytest_addoption(parser):
    parser.addoption(
        "--url",
        action="store",
        default="https://jsonplaceholder.typicode.com/todos",
        help="Request base url"
    )


@pytest.fixture(scope="module")
def base_url(request):
    url = request.config.getoption("--url")
    return url


@pytest.fixture(scope="module")
def session():
    return requests.Session()


# test case class for api test
class ApiTestCase:

    def __init__(self, base_url, session):
        self.base_url = base_url
        self.session = session

    def get(self, id=None, params=None):
        if id is None:
            return self.session.get(url=f'{self.base_url}', params=params)
        return self.session.get(url=f'{self.base_url}/{id}', params=params)

    def post(self, payload=None, params=None):
        return self.session.post(url=f'{self.base_url}',
                                 json=payload,
                                 params=params)

    def put(self, payload, id):
        return self.session.put(url=f'{self.base_url}/{id}',
                                json=payload)

    def patch(self, payload, id):
        return self.session.put(url=f'{self.base_url}/{id}',
                                json=payload)

    def delete(self, id):
        return self.session.delete(url=f'{self.base_url}/{id}')


@pytest.fixture(scope="module")
def api_test(session, base_url):
    return ApiTestCase(base_url, session)


@pytest.fixture(scope="module")
def all_todos_schema():
    with open("schemas/all_todos.schm") as f:
        yield json.load(f)


@pytest.fixture(scope="module")
def one_todos_schema():
    with open("schemas/one_todos.schm") as f:
        yield json.load(f)
