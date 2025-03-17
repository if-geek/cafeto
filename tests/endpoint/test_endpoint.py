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
        @app.get('/get')
        async def country_get(self) -> None:
            return NoContent()

    @app.controller('/home')
    class HomeController(BaseController):
        @app.get('/get')
        async def home_get(self) -> None:
            return NoContent()
        
        @app.post('/post')
        async def home_post(self) -> None:
            return NoContent()
        
        @app.put('/put')
        async def home_put(self) -> None:
            return NoContent()
        
        @app.patch('/patch')
        async def home_patch(self) -> None:
            return NoContent()
        
        @app.delete('/delete')
        async def home_delete(self) -> None:
            return NoContent()

    app.map_controllers()
    yield TestClient(app)


def test_controller_default_path(app_setup):
    client = app_setup
    response = client.get('/country/get')
    assert response.status_code == 204

def test_action_get(app_setup):
    client = app_setup
    response = client.get('/home/get')
    assert response.status_code == 204

def test_action_post(app_setup):
    client = app_setup
    response = client.post('/home/post')
    assert response.status_code == 204

def test_action_put(app_setup):
    client = app_setup
    response = client.put('/home/put')
    assert response.status_code == 204

def test_action_patch(app_setup):
    client = app_setup
    response = client.patch('/home/patch')
    assert response.status_code == 204

def test_action_delete(app_setup):
    client = app_setup
    response = client.delete('/home/delete')
    assert response.status_code == 204
