from typing import Any, Dict

import pytest

from cafeto import App, CafetoConfig
from cafeto.testclient import TestClient
from cafeto.responses import Ok
from cafeto.mvc import BaseController

from tests.data import (
    ModelRaiseErrorDto,
    ExtraModelRaiseErrorDto,
    assert_extra_model_raise_error,
    generate_extra_model_data,
    generate_model_data,
    assert_model_raise_error
)


@pytest.fixture(autouse=True)
def app_setup():
    cafeto_config = CafetoConfig(error_object=True)
    app: App = App(config=cafeto_config)

    @app.controller('/custom-raise-error')
    class CustomRaiseErrorController(BaseController):
        @app.post('/check-model')
        async def check_model(self, data: ModelRaiseErrorDto) -> Dict[str, Any]:
            return Ok(data.model_response())
        
        @app.post('/check-extra-model')
        async def check_extra_model(self, data: ExtraModelRaiseErrorDto) -> Dict[str, Any]:
            return Ok(data.model_response())
        
    app.map_controllers()
    yield TestClient(app)


def test_request_model_raise_error(app_setup):
    client = app_setup
    seed: int = 1

    data = generate_model_data(seed)
    response = client.post('/custom-raise-error/check-model', json=data)
    assert response.status_code == 400

    response = response.json()
    assert_model_raise_error(response['errorList'])


def test_request_extra_model_raise_error(app_setup):
    client = app_setup
    seed: int = 1

    data = generate_extra_model_data(seed)
    response = client.post('/custom-raise-error/check-extra-model', json=data)
    assert response.status_code == 400

    response = response.json()
    assert_extra_model_raise_error(response['errorList'])
