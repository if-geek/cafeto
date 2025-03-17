import pytest
from cafeto import App
from cafeto.testclient import TestClient
from cafeto.middleware import AuthenticationMiddleware
from cafeto.mvc import BaseController
from cafeto.responses import ModelResponse, JSONResponse, Response

from tests.data import LoginRequestDto, LoginResponseDto, TokenAuthBackend


@pytest.fixture(autouse=True)
def app_setup():
    app: App = App()

    app.add_middleware(AuthenticationMiddleware, backend=TokenAuthBackend())

    @app.controller('/auth')
    class AuthController(BaseController):

        @app.post('/login')
        async def login(self, data: LoginRequestDto) -> LoginResponseDto:
            if data.username == 'admin' and data.password == 'admin':
                token = TokenAuthBackend.token_admin
                return ModelResponse(LoginResponseDto(token=token))
            return Response(status_code=401)
        
        @app.get('/resource/{resource_name}')
        @app.requires('any_scope')
        async def get_resource(self, resource_name: str) -> JSONResponse:
            return JSONResponse({
                'resource': resource_name
            })
        
        @app.get('/admin/resource/{resource_name}')
        @app.requires('admin')
        async def get_admin_resource(self, resource_name: str) -> JSONResponse:
            return JSONResponse({
                'resource': resource_name
            })
        
    app.map_controllers()
    yield TestClient(app)


def test_login(app_setup):
    client = app_setup
    response = client.post('/auth/login', json={'username': 'admin', 'password': 'admin'})
    assert response.status_code == 200
    assert response.json() == {'token': TokenAuthBackend.token_admin}

def test_access_denied_no_token(app_setup):
    client = app_setup
    response = client.get('/auth/resource/my_resource')
    assert response.status_code == 403

def test_access_denied_wrong_token(app_setup):
    client = app_setup
    response = client.get('/auth/admin/resource/my_resource', headers={'Authorization': TokenAuthBackend.token_user})
    assert response.status_code == 403

def test_access_granted(app_setup):
    client = app_setup
    response = client.get('/auth/admin/resource/my_resource', headers={'Authorization': TokenAuthBackend.token_admin})
    assert response.status_code == 200
    assert response.json() == {'resource': 'my_resource'}
