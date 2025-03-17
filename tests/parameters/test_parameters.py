from typing import Any, Dict

import pytest

from cafeto import App
from cafeto.testclient import TestClient
from cafeto.responses import Ok
from cafeto.mvc import BaseController

from tests.data import ModelDto, generate_model_data


@pytest.fixture(autouse=True)
def app_setup():
    app: App = App()

    @app.controller()
    class ParamsController(BaseController):
        @app.get('/get-query', query=['id', 'name'])
        async def get_query(self, id: int, name: str) -> Dict[str, Any]:
            return Ok({'id': id, 'name': name})
        
        @app.get('/get-headers', headers=['token', 'language'])
        async def get_headers(self, token: str, language: str) -> Dict[str, Any]:
            return Ok({'token': token, 'language': language})
        
        @app.get('/get-query-default', query=['id', 'name'])
        async def get_query_defaults(self, id: int, name: str = 'Jane Doe') -> Dict[str, Any]:
            return Ok({'id': id, 'name': name})
        
        @app.get('/get-headers-default', headers=['token', 'language'])
        async def get_headers_defaults(self, token: str, language: str = 'en-US') -> Dict[str, Any]:
            return Ok({'token': token, 'language': language})
        
        @app.post('/post-query-headers/{group}', query=['id', 'name'], headers=['token', 'language'])
        async def post_query_headers(self, id: int, name: str, group: int, data: ModelDto, token: str, language: str) -> Dict[str, Any]:
            return Ok({
                'id': id,
                'name': name,
                'token': token,
                'group': group,
                'language': language,
                'data': {
                    'name': data.field_str,
                    'code': str(data.field_uuid)
                }
            })
        
    app.map_controllers()
    yield TestClient(app)


def test_controller_query_params(app_setup):
    client = app_setup
    response = client.get('/params/get-query', params={'id': '1', 'name': 'John Doe'})
    assert response.status_code == 200
    assert response.json() == {'id': 1, 'name': 'John Doe'}

def test_controller_headers_params(app_setup):
    client = app_setup
    response = client.get('/params/get-headers', headers={'token': '123456', 'language': 'es-CO'})
    assert response.status_code == 200
    assert response.json() == {'token': '123456', 'language': 'es-CO'}

def test_controller_query_default_params(app_setup):
    client = app_setup
    response = client.get('/params/get-query-default', params={'id': '1'})
    assert response.status_code == 200
    assert response.json() == {'id': 1, 'name': 'Jane Doe'}

def test_controller_headers_default_params(app_setup):
    client = app_setup
    response = client.get('/params/get-headers-default', headers={'token': '123456'})
    assert response.status_code == 200
    assert response.json() == {'token': '123456', 'language': 'en-US'}

def test_controller_post_query_headers_params(app_setup):
    client = app_setup
    seed: int = 1

    data = generate_model_data(seed)
    response = client.post('/params/post-query-headers/1', json=data, params={'id': '1', 'name': 'N.N.'}, headers={'token': '123456', 'language': 'es-CO'})
    assert response.status_code == 200
    assert response.json() == {
        'data': {
            'name': data['field_str'],
            'code': data['field_uuid']
        },
        'group': 1,
        'id': 1,
        'name': 'N.N.',
        'token': '123456',
        'language': 'es-CO'
    }
