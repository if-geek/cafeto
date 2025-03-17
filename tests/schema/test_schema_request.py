import pytest
from cafeto import App
from cafeto.testclient import TestClient
from cafeto.datastructures import UploadFile
from cafeto.responses import NoContent
from cafeto.mvc import BaseController

from tests.data import (
    ModelDto,
    ExtraModelDto
)


@pytest.fixture(autouse=True)
def app_setup():
    app: App = App()


    @app.controller('/schema-a')
    class SchemaAController(BaseController):
        @app.post('/request-model')
        async def request_model(self, data: ModelDto) -> None:
            return NoContent()

        @app.post('/request-upload')
        async def upload(self, file: UploadFile) -> None:
            return NoContent()

    @app.controller('/schema-b')
    class SchemaBController(BaseController):
        @app.post('/request-extra-model')
        async def request_extra_model(self, data: ExtraModelDto) -> None:
            return NoContent()


    app.map_controllers()
    app.use_schema()
    app.use_swagger()

    yield TestClient(app)


def get_schema(client):
    response = client.get('/schema/openapi.json')
    return response.json()

def test_request(app_setup):
    client = app_setup
    schema = get_schema(client)
    assert schema['paths']['/schema-a/request-model']['post']['requestBody']['content']['application/json']['schema']['$ref'] == '#/components/schemas/ModelDto'
    assert schema['paths']['/schema-b/request-extra-model']['post']['requestBody']['content']['application/json']['schema']['$ref'] == '#/components/schemas/ExtraModelDto'

def test_upload_file(app_setup):
    client = app_setup
    schema = get_schema(client)
    assert schema['paths']['/schema-a/request-upload']['post']['requestBody']['content']['multipart/form-data']['schema']['properties']['file']['type'] == 'string'
