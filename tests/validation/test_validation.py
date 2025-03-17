from typing import Any, Dict

import pytest

from cafeto import App
from cafeto.testclient import TestClient
from cafeto.mvc import BaseController
from cafeto.responses import Ok

from tests.data import (
    ExtraModelPydanticValidationsDto,
    ModelAlterDataDto,
    ModelDto,
    ModelRaiseErrorDto,
    ExtraModelAlterDataDto,
    ExtraModelRaiseErrorDto,
    assert_extra_model_raise_error,
    assert_pydantic_model_raise_error,
    generate_extra_model_data,
    assert_extra_model_alter_data,
    generate_model_data,
    assert_model_alter_data,
    assert_model_raise_error
)


@pytest.fixture(autouse=True)
def app_setup():
    app: App = App()

    @app.controller('/custom-alter-data')
    class CustomAlterDataController(BaseController):
        @app.post('/check-model')
        async def check_model(self, data: ModelAlterDataDto) -> Dict[str, Any]:
            return Ok(data.model_response())
        
        @app.post('/check-extra-model')
        async def check_extra_model(self, data: ExtraModelAlterDataDto) -> Dict[str, Any]:
            return Ok(data.model_response())


    @app.controller('/custom-raise-error')
    class CustomRaiseErrorController(BaseController):
        @app.post('/check-model')
        async def check_model(self, data: ModelRaiseErrorDto) -> Dict[str, Any]:
            return Ok(data.model_response())
        
        @app.post('/check-extra-model')
        async def check_extra_model(self, data: ExtraModelRaiseErrorDto) -> Dict[str, Any]:
            return Ok(data.model_response())
        

    @app.controller('/pydantic')
    class PydanticController(BaseController):
        @app.post('/check-model')
        async def check_model(self, data: ModelDto) -> Dict[str, Any]:
            return Ok(data.model_response())
        

    @app.controller('/model-raise-error')
    class ModelRaiseErrorController(BaseController):
        @app.post('/check-model-pydantic-validations')
        async def check_model_pydantic_validations(self, data: ExtraModelPydanticValidationsDto) -> Dict[str, Any]:
            return Ok(data.model_response())
        

    app.map_controllers()
    yield TestClient(app)


def test_request_model_alter_data(app_setup):
    client = app_setup
    seed: int = 1

    data = generate_model_data(seed)
    response = client.post('/custom-alter-data/check-model', json=data)
    assert response.status_code == 200

    response = response.json()
    assert_model_alter_data(response, seed)


def test_request_extra_model_alter_data(app_setup):
    client = app_setup
    seed: int = 1

    data = generate_extra_model_data(seed)
    response = client.post('/custom-alter-data/check-extra-model', json=data)
    assert response.status_code == 200

    response = response.json()
    assert_extra_model_alter_data(response, seed)


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


def test_request_pydantic_model(app_setup):
    client = app_setup
    response = client.post('/pydantic/check-model', json={})
    assert response.status_code == 400

    response = response.json()
    assert_pydantic_model_raise_error(response['errorList'])


def test_request_pydantic_model_fild_dict_models(app_setup):
    client = app_setup
    data = {}
    data['field_model'] = {}
    data['field_model_list'] = [{}, {}]
    data['field_model_dict'] = {
        'key 1': {},
        'key 2': {}
    }

    response = client.post('/model-raise-error/check-model-pydantic-validations', json=data)
    assert response.status_code == 400

    response = response.json()
    assert_pydantic_model_raise_error(response['errorList'], ['field_model'])
    assert_pydantic_model_raise_error(response['errorList'], ['field_model_list', 0])
    assert_pydantic_model_raise_error(response['errorList'], ['field_model_list', 1])
    assert_pydantic_model_raise_error(response['errorList'], ['field_model_dict', 'key 1'])
    assert_pydantic_model_raise_error(response['errorList'], ['field_model_dict', 'key 2'])
