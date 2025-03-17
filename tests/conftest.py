import pytest

from starlette.testclient import TestClient
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware import Middleware


from cafeto.app import App
from tests.data import TokenAuthBackend


@pytest.fixture(scope="module")
def app():
    app: App = App()
    yield app


@pytest.fixture(scope="module")
def client(app: App):
    return TestClient(app)
