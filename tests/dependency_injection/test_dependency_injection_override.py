from typing import Dict

import pytest

from cafeto import App, responses
from cafeto.dependency_injection.service_collection import ServiceCollection
from cafeto.testclient import TestClient
from cafeto.mvc import BaseController

from tests.data import (
    UServiceOriginal,
    ServiceOriginal,
    ServiceOverride
)


@pytest.fixture(autouse=True)
def app_setup():
    app: App = App()

    @app.controller()
    class DependencyController(BaseController):

        @app.get('/get-singleton')
        async def singleton(self, service: UServiceOriginal) -> Dict[str, str]:
            return responses.Ok({'data': service.data})
        
        @app.get('/get-scoped')
        async def scoped(self, service: UServiceOriginal) -> Dict[str, str]:
            return responses.Ok({'data': service.data})
        
        @app.get('/get-transient')
        async def transient(self, service: UServiceOriginal) -> Dict[str, str]:
            return responses.Ok({'data': service.data})


    app.map_controllers()
    app.add_singleton(UServiceOriginal, ServiceOriginal)
    app.add_scoped(UServiceOriginal, ServiceOriginal)
    app.add_transient(UServiceOriginal, ServiceOriginal)
    

    yield TestClient(app)


@pytest.fixture()
def app_setup_override(app_setup):
    client = app_setup
    app: App = client.app
    app.add_singleton(UServiceOriginal, ServiceOverride, override = True)
    app.add_scoped(UServiceOriginal, ServiceOverride, override = True)
    app.add_transient(UServiceOriginal, ServiceOverride, override = True)

    yield client


@pytest.fixture()
def app_setup_remove(app_setup):
    client = app_setup
    app: App = client.app
    app.remove_singleton(UServiceOriginal)
    app.remove_scoped(UServiceOriginal)
    app.remove_transient(UServiceOriginal)

    yield client


def test_singleton(app_setup):
    client = app_setup
    response = client.get('/dependency/get-singleton')
    assert response.status_code == 200
    assert response.json() == {'data': 'Original'}


def test_scoped(app_setup):
    client = app_setup
    response = client.get('/dependency/get-scoped')
    assert response.status_code == 200
    assert response.json() == {'data': 'Original'}


def test_transient(app_setup):
    client = app_setup
    response = client.get('/dependency/get-transient')
    assert response.status_code == 200
    assert response.json() == {'data': 'Original'}


def test_singleton_override(app_setup_override):
    client = app_setup_override
    response = client.get('/dependency/get-singleton')
    assert response.status_code == 200
    assert response.json() == {'data': 'Override'}


def test_scoped_override(app_setup_override):
    client = app_setup_override
    response = client.get('/dependency/get-scoped')
    assert response.status_code == 200
    assert response.json() == {'data': 'Override'}


def test_transient_override(app_setup_override):
    client = app_setup_override
    response = client.get('/dependency/get-transient')
    assert response.status_code == 200
    assert response.json() == {'data': 'Override'}


def test_singleton_remove(app_setup_remove):
    assert ServiceCollection.singleton.get(UServiceOriginal, None) is None


def test_scoped_remove(app_setup_remove):
    assert ServiceCollection.scoped.get(UServiceOriginal, None) is None


def test_transient_remove(app_setup_remove):
    assert ServiceCollection.transient.get(UServiceOriginal, None) is None
