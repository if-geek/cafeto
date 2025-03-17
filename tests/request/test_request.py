from typing import Any, Dict

import pytest

from cafeto import App
from cafeto.testclient import TestClient
from cafeto.datastructures import UploadFile
from cafeto.mvc import BaseController
from cafeto.responses import Ok

from tests.data import (
    ModelDto,
    ExtraModelDto,
    assert_model,
    generate_model_data,
    assert_extra_model,
    generate_extra_model_data
)


@pytest.fixture(autouse=True)
def app_setup():
    app: App = App()

    @app.controller('/custom')
    class CustomController(BaseController):
        @app.post('/check-model')
        async def check_model(self, data: ModelDto) -> Dict[str, Any]:
            return Ok(data.model_response())
        
        @app.post('/check-extra-model')
        async def check_extra_model(self, data: ExtraModelDto) -> Dict[str, Any]:
            return Ok(data.model_response())
        
        @app.post('/upload')
        async def upload(self, file: UploadFile) -> Dict[str, str]:
            return Ok({'file': file.filename})
        

    app.map_controllers()
    yield TestClient(app)


def test_request_check_model(app_setup):
    client = app_setup
    seed: int = 1

    data = generate_model_data(seed)
    response = client.post('/custom/check-model', json=data)
    assert response.status_code == 200

    response = response.json()
    assert_model(response, seed)


def test_request_extra_model(app_setup):
    client = app_setup
    seed: int = 1

    data = generate_extra_model_data(seed)
    response = client.post('/custom/check-extra-model', json=data)
    assert response.status_code == 200

    response = response.json()
    assert_extra_model(response, seed)


def test_request_upload(app_setup):
    client = app_setup
    response = client.post('/custom/upload', files={'file': ('test.txt', b'hello world')})
    assert response.status_code == 200
    assert response.json() == {'file': 'test.txt'}
