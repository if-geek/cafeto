from typing import Any, Dict

import pytest

from cafeto import App
from cafeto.errors.errors import ModelError
from cafeto.requests.request import format_errors
from cafeto.responses.unified_response import BadRequest
from cafeto.testclient import TestClient
from cafeto.mvc import BaseController
from cafeto.responses import Ok

from tests.data import (
    ExtraModelAlterDataValidator,
    ExtraModelDto,
    ExtraModelRaiseErrorValidator,
    ModelAlterDataValidator,
    ModelDto,
    ModelRaiseErrorValidator,
    assert_extra_model_raise_error,
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
        @app.post('/check-model', body={'validator': ModelAlterDataValidator})
        async def check_model(self, data: ModelDto) -> Dict[str, Any]:
            return Ok(data.model_response())
        
        @app.post('/check-extra-model', body={'validator': ExtraModelAlterDataValidator})
        async def check_extra_model(self, data: ExtraModelDto) -> Dict[str, Any]:
            return Ok(data.model_response())


    @app.controller('/custom-raise-error')
    class CustomRaiseErrorController(BaseController):
        @app.post('/check-model', body={'validator': ModelRaiseErrorValidator})
        async def check_model(self, data: ModelDto) -> Dict[str, Any]:
            return Ok(data.model_response())
        
        @app.post('/check-extra-model', body={'validator': ExtraModelRaiseErrorValidator})
        async def check_extra_model(self, data: ExtraModelDto) -> Dict[str, Any]:
            return Ok(data.model_response())


    @app.controller('/custom-no-validate')
    class CustomAlterDataController(BaseController):
        @app.post('/check-model', body={'validator': None})
        async def check_model_no_validate(self, data: ModelDto) -> Dict[str, Any]:
            return Ok(data.model_response())
        
        @app.post('/check-error-model', body={'validator': None})
        async def check_error_model(self, data: ModelDto) -> Dict[str, Any]:
            try:
                await data.check(ModelAlterDataValidator)
            except ModelError as e:
                errors = format_errors(e.errors)
                return BadRequest(errors)


    app.map_controllers()
    yield TestClient(app)


def test_request_model_alter_data_custom_validator(app_setup):
    client = app_setup
    seed: int = 1

    data = generate_model_data(seed)
    response = client.post('/custom-alter-data/check-model', json=data)
    assert response.status_code == 200

    response = response.json()
    assert_model_alter_data(response, seed)


def test_request_extra_model_alter_data_custom_validator(app_setup):
    client = app_setup
    seed: int = 1

    data = generate_extra_model_data(seed)
    
    response = client.post('/custom-alter-data/check-extra-model', json=data)
    assert response.status_code == 200

    response = response.json()
    assert_extra_model_alter_data(response, seed)


def test_request_model_raise_error_custom_validator(app_setup):
    client = app_setup
    seed: int = 1

    data = generate_model_data(seed)
    response = client.post('/custom-raise-error/check-model', json=data)
    assert response.status_code == 400

    response = response.json()
    assert_model_raise_error(response['errorList'])


def test_request_extra_model_raise_error_custom_validator(app_setup):
    client = app_setup
    seed: int = 1

    data = generate_extra_model_data(seed)
    response = client.post('/custom-raise-error/check-extra-model', json=data)
    assert response.status_code == 400

    response = response.json()
    assert_extra_model_raise_error(response['errorList'])


def test_request_model_no_validate(app_setup):
    client = app_setup

    response = client.post('/custom-no-validate/check-model', json={})
    assert response.status_code == 200

    response = response.json()
    assert response['field_str'] == None
    assert response['field_uuid'] == None
    assert response['field_int'] == None
    assert response['field_float'] == None
    assert response['field_bool'] == None
    assert response['field_dict'] == None
    assert response['field_list'] == None
    assert response['field_date'] == None
    assert response['field_time'] == None


def test_request_error_model(app_setup):
    client = app_setup

    response = client.post('/custom-no-validate/check-error-model', json={})
    assert response.status_code == 400

    response = response.json()
    assert response['errorList'][0]['type'] == 'missing'
    assert response['errorList'][0]['msg'] == 'Field required'
    assert response['errorList'][0]['loc'] == ['field_str']

    assert response['errorList'][1]['type'] == 'missing'
    assert response['errorList'][1]['msg'] == 'Field required'
    assert response['errorList'][1]['loc'] == ['field_uuid']

    assert response['errorList'][2]['type'] == 'missing'
    assert response['errorList'][2]['msg'] == 'Field required'
    assert response['errorList'][2]['loc'] == ['field_int']

    assert response['errorList'][3]['type'] == 'missing'
    assert response['errorList'][3]['msg'] == 'Field required'
    assert response['errorList'][3]['loc'] == ['field_float']
