import pytest
from cafeto import App
from cafeto.testclient import TestClient
from cafeto import responses
from cafeto.mvc import BaseController


@pytest.fixture(autouse=True)
def app_setup():
    app: App = App()

    @app.controller()
    class SchemaController(BaseController):
        @app.get('/get')
        async def create(self) -> None:
            return responses.NoContent()


    app.map_controllers()
    app.use_schema()
    app.use_swagger()

    yield TestClient(app)


def test_api_json(app_setup):
    client = app_setup
    response = client.get('/schema/openapi.json')
    assert response.status_code == 200

def test_api_yaml(app_setup):
    client = app_setup
    response = client.get('/schema/openapi.yaml')
    assert response.status_code == 200

def test_api_swagger(app_setup):
    client = app_setup
    response = client.get('/schema/swagger-ui.html')
    assert response.status_code == 200
