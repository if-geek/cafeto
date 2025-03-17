import pytest
from cafeto import App
from cafeto.testclient import TestClient
from cafeto.responses import NoContent
from cafeto.mvc import BaseController
from cafeto.schema import ExternalDocs

@pytest.fixture(autouse=True)
def app_setup():
    app: App = App()

    @app.controller()
    class SchemaController(BaseController):
        @app.get('/get')
        async def get(self) -> None:
            return NoContent()

    app.map_controllers()
    app.use_schema(
        external_docs=ExternalDocs(url='http://127.0.0.1', description='Schema documentation')
    )
    app.use_swagger()


    yield TestClient(app)

def get_schema(client):
    response = client.get('/schema/openapi.json')
    return response.json()

def test_external_docs(app_setup):
    client = app_setup
    schema = get_schema(client)
    assert schema['externalDocs'] == {'url': 'http://127.0.0.1', 'description': 'Schema documentation'}
