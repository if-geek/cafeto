import uuid

from typing import Dict

import pytest

from cafeto import App
from cafeto.testclient import TestClient
from cafeto.responses import Ok
from cafeto.mvc import BaseController


@pytest.fixture(autouse=True)
def app_setup():
    app: App = App()

    @app.controller()
    class CountryController(BaseController):
        @app.get('/get/{name}')
        async def country_get_name(self, name: str) -> Dict[str, str]:
            return Ok({'name': name})

    @app.controller('/home')
    class HomeController(BaseController):
        @app.get('/get/{id}')
        async def home_get_id(self, id: int) -> Dict[str, str]:
            return Ok({'id': id})
        
        @app.post('/post/{id}')
        async def home_post_id(self, id: int) -> Dict[str, str]:
            return Ok({'id': id})
        
        @app.post('/post-uuid/{id}')
        async def home_post_id_uuid(self, id: uuid.UUID) -> Dict[str, str]:
            return Ok({'id': str(id)})
        
        @app.put('/put/{id}')
        async def home_put_id(self, id: int) -> Dict[str, str]:
            return Ok({'id': id})
        
        @app.patch('/patch/{id}')
        async def home_patch_id(self, id: int) -> Dict[str, str]:
            return Ok({'id': id})
        
        @app.delete('/delete/{id}')
        async def home_delete_id(self, id: int) -> Dict[str, str]:
            return Ok({'id': id})
        
        @app.get('/get/{id}/{group}')
        async def home_get_multiple_params(self, id: int, group: str) -> Dict[str, str]:
            return Ok({'id': id, 'group': group})
        
        @app.get('/get/{id}/more-path/{group}')
        async def home_get_multiple_params_2(self, id: int, group: str) -> Dict[str, str]:
            return Ok({'id': id, 'group': group})
        
    app.map_controllers()
    yield TestClient(app)


def test_controller_default_path(app_setup):
    client = app_setup
    response = client.get('/country/get/Colombia')
    assert response.status_code == 200
    assert response.json() == {'name': 'Colombia'}

def test_action_get_id(app_setup):
    client = app_setup
    response = client.get('/home/get/1')
    assert response.status_code == 200
    assert response.json() == {'id': 1}

def test_action_get_id_uuid(app_setup):
    client = app_setup
    id = str(uuid.uuid4())
    response = client.post(f'/home/post-uuid/{id}')
    assert response.status_code == 200
    assert response.json() == {'id': id}

def test_action_post_id(app_setup):
    client = app_setup
    response = client.post('/home/post/1')
    assert response.status_code == 200
    assert response.json() == {'id': 1}

def test_action_put_id(app_setup):
    client = app_setup
    response = client.put('/home/put/1')
    assert response.status_code == 200
    assert response.json() == {'id': 1}

def test_action_patch_id(app_setup):
    client = app_setup
    response = client.patch('/home/patch/1')
    assert response.status_code == 200
    assert response.json() == {'id': 1}

def test_action_delete_id(app_setup):
    client = app_setup
    response = client.delete('/home/delete/1')
    assert response.status_code == 200
    assert response.json() == {'id': 1}

def test_action_get_multiple_params(app_setup):
    client = app_setup
    response = client.get('/home/get/1/users')
    assert response.status_code == 200
    assert response.json() == {'id': 1, 'group': 'users'}

def test_action_get_multiple_params_2(app_setup):
    client = app_setup
    response = client.get('/home/get/1/more-path/users')
    assert response.status_code == 200
    assert response.json() == {'id': 1, 'group': 'users'}
