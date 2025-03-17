from typing import Any, Dict
import pytest

from cafeto import App
from cafeto.responses.unified_response import Ok
from cafeto.services.context_service import AContextService
from cafeto.testclient import TestClient
from cafeto.mvc import BaseController
from tests.data import ModelDto, assert_model, generate_extra_model_data


@pytest.fixture(autouse=True)
def app_setup():
    app: App = App()

    @app.controller()
    class HomeController(BaseController):
        @app.post('/home')
        async def home(self, request_model: ModelDto, context_service: AContextService) -> Dict[str, Any]:
            return Ok(context_service.to_json())

    app.map_controllers()
    app.use_default_services()

    yield TestClient(app)


def test_context_service(app_setup):
    seed: int = 1
    
    client = app_setup
    data = generate_extra_model_data(seed)
    response = client.post(f'/home/home', json=data)
    assert response.status_code == 200
    response = response.json()


    assert response['controller_name'] == 'HomeController'
    assert response['action_name'] == 'home'
    assert response['path'] == '/home/home'
    assert response['method'] == 'POST'
    assert_model(response['request_model'] , seed)
