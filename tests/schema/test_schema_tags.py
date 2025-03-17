import pytest
from cafeto import App
from cafeto.testclient import TestClient
from cafeto.responses import NoContent
from cafeto.mvc import BaseController


@pytest.fixture(autouse=True)
def app_setup():
    app: App = App()

    @app.controller('/schema-a')
    class SchemaAController(BaseController):
        @app.post('/check')
        async def check(self) -> None:
            return NoContent()

    @app.controller('/schema-b')
    class SchemaBController(BaseController):
        @app.post('/check')
        async def check(self) -> None:
            return NoContent()


    app.map_controllers()
    app.use_schema()
    app.use_swagger()

    yield TestClient(app)


def get_schema(client):
    response = client.get('/schema/openapi.json')
    return response.json()

def test_tags(app_setup):
    client = app_setup
    schema = get_schema(client)
    assert len(schema['tags']) == 2

def test_paths_tags(app_setup):
    client = app_setup
    schema = get_schema(client)
    assert schema['paths']['/schema-a/check']['post']['tags'] == ['SchemaAController']
    assert schema['paths']['/schema-b/check']['post']['tags'] == ['SchemaBController']
    