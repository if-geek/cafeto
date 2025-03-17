import uuid

import pytest

from cafeto import App
from cafeto.testclient import TestClient
from cafeto.responses import NoContent
from cafeto.mvc import BaseController


@pytest.fixture(autouse=True)
def app_setup():
    app: App = App()

    @app.controller()
    class SchemaController(BaseController):
        @app.get('/path-param/{id}')
        async def get(self, id: uuid.UUID) -> None:
            return NoContent()

        @app.get('/path-multiple-param/{id}/{name}/{pos}')
        async def get(self, id: int, name: str, pos: float) -> None:
            return NoContent()

        @app.get('/query-param', query=['id', 'name'])
        async def get(self, id: int, name: str) -> None:
            return NoContent()

        @app.get('/query-param/optional', query=['id', 'name'])
        async def get(self, id: int, name: str = 'optional') -> None:
            return NoContent()

        @app.get('/header-param', headers=['token', 'language'])
        async def get(self, token: str, language: str) -> None:
            return NoContent()

        @app.get('/header-param/optional', headers=['token', 'language'])
        async def get(self, token: str, language: str = 'optional') -> None:
            return NoContent()


    app.map_controllers()
    app.use_schema()
    app.use_swagger()

    yield TestClient(app)


def get_schema(client):
    response = client.get('/schema/openapi.json')
    return response.json()
 
def test_path_param(app_setup):
    client = app_setup
    schema = get_schema(client)
    assert schema['paths']['/schema/path-param/{id}']['get']['parameters'][0]['name'] == 'id'
    assert schema['paths']['/schema/path-param/{id}']['get']['parameters'][0]['in'] == 'path'
    assert schema['paths']['/schema/path-param/{id}']['get']['parameters'][0]['required'] == True
    assert schema['paths']['/schema/path-param/{id}']['get']['parameters'][0]['schema']['type'] == 'string'
    assert schema['paths']['/schema/path-param/{id}']['get']['parameters'][0]['schema']['format'] == 'uuid'

def test_param_multiple(app_setup):
    client = app_setup
    schema = get_schema(client)
    assert schema['paths']['/schema/path-multiple-param/{id}/{name}/{pos}']['get']['parameters'][0]['name'] == 'id'
    assert schema['paths']['/schema/path-multiple-param/{id}/{name}/{pos}']['get']['parameters'][0]['in'] == 'path'
    assert schema['paths']['/schema/path-multiple-param/{id}/{name}/{pos}']['get']['parameters'][0]['required'] == True
    assert schema['paths']['/schema/path-multiple-param/{id}/{name}/{pos}']['get']['parameters'][0]['schema']['type'] == 'number'
    assert schema['paths']['/schema/path-multiple-param/{id}/{name}/{pos}']['get']['parameters'][0]['schema']['format'] == 'integer'

    assert schema['paths']['/schema/path-multiple-param/{id}/{name}/{pos}']['get']['parameters'][1]['name'] == 'name'
    assert schema['paths']['/schema/path-multiple-param/{id}/{name}/{pos}']['get']['parameters'][1]['in'] == 'path'
    assert schema['paths']['/schema/path-multiple-param/{id}/{name}/{pos}']['get']['parameters'][1]['required'] == True
    assert schema['paths']['/schema/path-multiple-param/{id}/{name}/{pos}']['get']['parameters'][1]['schema']['type'] == 'string'
    assert schema['paths']['/schema/path-multiple-param/{id}/{name}/{pos}']['get']['parameters'][1]['schema']['format'] == 'string'

    assert schema['paths']['/schema/path-multiple-param/{id}/{name}/{pos}']['get']['parameters'][2]['name'] == 'pos'
    assert schema['paths']['/schema/path-multiple-param/{id}/{name}/{pos}']['get']['parameters'][2]['in'] == 'path'
    assert schema['paths']['/schema/path-multiple-param/{id}/{name}/{pos}']['get']['parameters'][2]['required'] == True
    assert schema['paths']['/schema/path-multiple-param/{id}/{name}/{pos}']['get']['parameters'][2]['schema']['type'] == 'number'
    assert schema['paths']['/schema/path-multiple-param/{id}/{name}/{pos}']['get']['parameters'][2]['schema']['format'] == 'float'

def test_query_param(app_setup):
    client = app_setup
    schema = get_schema(client)
    assert schema['paths']['/schema/query-param']['get']['parameters'][0]['name'] == 'id'
    assert schema['paths']['/schema/query-param']['get']['parameters'][0]['in'] == 'query'
    assert schema['paths']['/schema/query-param']['get']['parameters'][0]['required'] == True
    assert schema['paths']['/schema/query-param']['get']['parameters'][0]['schema']['type'] == 'number'
    assert schema['paths']['/schema/query-param']['get']['parameters'][0]['schema']['format'] == 'integer'

    assert schema['paths']['/schema/query-param']['get']['parameters'][1]['name'] == 'name'
    assert schema['paths']['/schema/query-param']['get']['parameters'][1]['in'] == 'query'
    assert schema['paths']['/schema/query-param']['get']['parameters'][1]['required'] == True
    assert schema['paths']['/schema/query-param']['get']['parameters'][1]['schema']['type'] == 'string'
    assert schema['paths']['/schema/query-param']['get']['parameters'][1]['schema']['format'] == 'string'

def test_query_param_optional(app_setup):
    client = app_setup
    schema = get_schema(client)
    assert schema['paths']['/schema/query-param/optional']['get']['parameters'][0]['name'] == 'id'
    assert schema['paths']['/schema/query-param/optional']['get']['parameters'][0]['in'] == 'query'
    assert schema['paths']['/schema/query-param/optional']['get']['parameters'][0]['required'] == True
    assert schema['paths']['/schema/query-param/optional']['get']['parameters'][0]['schema']['type'] == 'number'
    assert schema['paths']['/schema/query-param/optional']['get']['parameters'][0]['schema']['format'] == 'integer'

    assert schema['paths']['/schema/query-param/optional']['get']['parameters'][1]['name'] == 'name'
    assert schema['paths']['/schema/query-param/optional']['get']['parameters'][1]['in'] == 'query'
    assert schema['paths']['/schema/query-param/optional']['get']['parameters'][1]['required'] == False
    assert schema['paths']['/schema/query-param/optional']['get']['parameters'][1]['schema']['type'] == 'string'
    assert schema['paths']['/schema/query-param/optional']['get']['parameters'][1]['schema']['format'] == 'string'

def test_header_param(app_setup):
    client = app_setup
    schema = get_schema(client)
    assert schema['paths']['/schema/header-param']['get']['parameters'][0]['name'] == 'token'
    assert schema['paths']['/schema/header-param']['get']['parameters'][0]['in'] == 'header'
    assert schema['paths']['/schema/header-param']['get']['parameters'][0]['required'] == True
    assert schema['paths']['/schema/header-param']['get']['parameters'][0]['schema']['type'] == 'string'
    assert schema['paths']['/schema/header-param']['get']['parameters'][0]['schema']['format'] == 'string'

    assert schema['paths']['/schema/header-param']['get']['parameters'][1]['name'] == 'language'
    assert schema['paths']['/schema/header-param']['get']['parameters'][1]['in'] == 'header'
    assert schema['paths']['/schema/header-param']['get']['parameters'][1]['required'] == True
    assert schema['paths']['/schema/header-param']['get']['parameters'][1]['schema']['type'] == 'string'
    assert schema['paths']['/schema/header-param']['get']['parameters'][1]['schema']['format'] == 'string'

def test_header_param_optional(app_setup):
    client = app_setup
    schema = get_schema(client)
    assert schema['paths']['/schema/header-param/optional']['get']['parameters'][0]['name'] == 'token'
    assert schema['paths']['/schema/header-param/optional']['get']['parameters'][0]['in'] == 'header'
    assert schema['paths']['/schema/header-param/optional']['get']['parameters'][0]['required'] == True
    assert schema['paths']['/schema/header-param/optional']['get']['parameters'][0]['schema']['type'] == 'string'
    assert schema['paths']['/schema/header-param/optional']['get']['parameters'][0]['schema']['format'] == 'string'

    assert schema['paths']['/schema/header-param/optional']['get']['parameters'][1]['name'] == 'language'
    assert schema['paths']['/schema/header-param/optional']['get']['parameters'][1]['in'] == 'header'
    assert schema['paths']['/schema/header-param/optional']['get']['parameters'][1]['required'] == False
    assert schema['paths']['/schema/header-param/optional']['get']['parameters'][1]['schema']['type'] == 'string'
    assert schema['paths']['/schema/header-param/optional']['get']['parameters'][1]['schema']['format'] == 'string'
