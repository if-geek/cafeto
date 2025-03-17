from typing import Dict

import pytest

from cafeto import App
from cafeto.testclient import TestClient
from cafeto.responses import Ok
from cafeto.mvc import BaseController
from cafeto.schema import SecurityScheme


@pytest.fixture(autouse=True)
def app_setup():
    app: App = App()

    @app.controller()
    class SchemaController(BaseController):
        @app.get('/get')
        @app.requires('admin')
        async def get(self) -> Dict:
            return Ok({'hello': 'world'})

    app.map_controllers()
    app.use_schema(
        security_scheme=SecurityScheme(name='appAuth', type='apiKey', in_='header', bearer_format='JWT')
    )
    app.use_swagger()

    yield TestClient(app)


def get_schema(client):
    response = client.get('/schema/openapi.json')
    return response.json()

def test_security(app_setup):
    client = app_setup
    schema = get_schema(client)
    assert schema['components']['securitySchemes'] == {'appAuth': {'type': 'apiKey', 'name': 'appAuth', 'in': 'header', 'bearerFormat': 'JWT'}}


def test_security_in_action(app_setup):
    client = app_setup
    schema = get_schema(client)
    assert schema['paths']['/schema/get']['get']['security'] == [{'appAuth': ['admin']}]
