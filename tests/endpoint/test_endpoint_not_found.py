import pytest
from cafeto import App
from cafeto.testclient import TestClient
from cafeto.responses import NoContent
from cafeto.mvc import BaseController


@pytest.fixture(autouse=True)
def app_setup():
    app: App = App()

    @app.controller()
    class CountryController(BaseController):
        @app.get('/get/{id}')
        async def country_get(self, id: int) -> None:
            return NoContent()
        
        @app.get('/get-all')
        async def country_get(self) -> None:
            return NoContent()
        
    app.map_controllers()
    yield TestClient(app)


def test_not_found_path_param(app_setup):
    client = app_setup
    response = client.delete('/country/get')
    assert response.status_code == 404

def test_not_found(app_setup):
    client = app_setup
    response = client.delete('/country/get-all-404')
    assert response.status_code == 404
