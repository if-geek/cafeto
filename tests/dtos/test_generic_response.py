from typing import Any, Dict, List

import pytest

from cafeto import App
from cafeto.testclient import TestClient
from cafeto.mvc import BaseController
from cafeto.responses import Ok
from cafeto.responses.formats import TEXT_HTML
from cafeto.dtos import GenericResponseDto

from tests.data import ModelDto, assert_model, generate_model_data


@pytest.fixture(autouse=True)
def app_setup():
    app: App = App()


    @app.controller()
    class GenericController(BaseController):
        @app.get('/model-generic-response/{seed}')
        async def country_generic_model(self, seed: int) -> GenericResponseDto[ModelDto]:
            return Ok(GenericResponseDto(data=ModelDto(**generate_model_data(seed))))
        
        @app.get('/model-generic-list-response/{seed_1}/{seed_2}')
        async def country_generic_list_model(self, seed_1: int, seed_2: int) -> GenericResponseDto[List[ModelDto]]:
            return Ok(
                GenericResponseDto(
                    data=[ModelDto(**generate_model_data(seed_1)), ModelDto(**generate_model_data(seed_2))]
                )
            )

    app.map_controllers()
    yield TestClient(app)


def test_model_generic_response(app_setup):
    client = app_setup
    seed: int = 1

    response = client.get(f'/generic/model-generic-response/{seed}')
    assert response.status_code == 200
    response = response.json()
    assert_model(response['data'], seed)


def test_model_list_generic_response(app_setup):
    client = app_setup
    seed_1: int = 1
    seed_2: int = 2

    response = client.get(f'/generic/model-generic-list-response/{seed_1}/{seed_2}')
    assert response.status_code == 200
    response = response.json()
    assert_model(response['data'][0], seed_1)
    assert_model(response['data'][1], seed_2)
