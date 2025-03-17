import pytest
from cafeto import App
from cafeto.testclient import TestClient
from cafeto.responses import NoContent
from cafeto.mvc import BaseController

from tests.data import (
    ExtraModelDto,
    ModelDto
)

@pytest.fixture(autouse=True)
def app_setup():
    app: App = App()

    @app.controller()
    class SchemaController(BaseController):
        @app.post('/create-model')
        async def create_model(self, data: ModelDto) -> ModelDto:
            return NoContent()
        
        @app.post('/create-extra-model')
        async def create_extra_model(self, data: ExtraModelDto) -> ExtraModelDto:
            return NoContent()
    

    app.map_controllers()
    app.use_schema()
    app.use_swagger()


    yield TestClient(app)

def get_schema(client):
    response = client.get('/schema/openapi.json')
    return response.json()

def test_components(app_setup):
    client = app_setup
    schema = get_schema(client)
    assert len(schema['components']['schemas']) == 2
    assert 'ModelDto' in schema['components']['schemas']
    assert 'ExtraModelDto' in schema['components']['schemas']


def test_components_refs(app_setup):
    client = app_setup
    schema = get_schema(client)
    assert schema['paths']['/schema/create-model']['post']['responses']['200']['content']['application/json']['schema']['$ref'] == '#/components/schemas/ModelDto'
    assert schema['paths']['/schema/create-model']['post']['requestBody']['content']['application/json']['schema']['$ref'] == '#/components/schemas/ModelDto'
    assert schema['paths']['/schema/create-extra-model']['post']['responses']['200']['content']['application/json']['schema']['$ref'] == '#/components/schemas/ExtraModelDto'
    assert schema['paths']['/schema/create-extra-model']['post']['requestBody']['content']['application/json']['schema']['$ref'] == '#/components/schemas/ExtraModelDto'
    assert schema['components']['schemas']['ExtraModelDto']['properties']['field_model']['$ref'] == '#/components/schemas/ModelDto'
    assert schema['components']['schemas']['ExtraModelDto']['properties']['field_model']['$ref'] == '#/components/schemas/ModelDto'


def test_components_list(app_setup):
    client = app_setup
    schema = get_schema(client)
    assert schema['components']['schemas']['ExtraModelDto']['type'] == 'object'
    assert schema['components']['schemas']['ExtraModelDto']['properties']['field_model_list']['type'] == 'array'
    assert schema['components']['schemas']['ExtraModelDto']['properties']['field_model_list']['items']['$ref'] == '#/components/schemas/ModelDto'
    