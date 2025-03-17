from typing import Dict, List

import pytest

from cafeto import App
from cafeto.testclient import TestClient
from cafeto.responses import NoContent, Ok, Format, formats
from cafeto.mvc import BaseController

from tests.data import (
    ModelDto,
    generate_model_data
)


@pytest.fixture(autouse=True)
def app_setup():
    app: App = App()

    @app.controller()
    class ResponseController(BaseController):
        @app.get('/model-response')
        async def model_response(self) -> ModelDto:
            return Ok(ModelDto(**generate_model_data(1)))

        @app.get('/model-list-response')
        async def model_list_response(self) -> List[ModelDto]:
            return Ok([
                ModelDto(**generate_model_data(1)),
                ModelDto(**generate_model_data(2))
            ])

        @app.get('/json-response')
        async def json_response(self) -> Dict[str ,str]:
            return Ok(generate_model_data(1))

        @app.get('/plain-text-response')
        async def plain_text_response(self) -> str:
            return Ok('Hello, World!')

        @app.get('/html-response')
        async def html_response(self) -> Format[str, formats.TEXT_HTML]:
            return Ok('<div>Hello, World!</div>')

        @app.get('/empty-response')
        async def empty_response(self) -> None:
            return NoContent()


    app.map_controllers()
    app.use_schema()
    app.use_swagger()

    yield TestClient(app)


def get_schema(client):
    response = client.get('/schema/openapi.json')
    return response.json()

def test_model_response_unified_style(app_setup):
    client = app_setup
    schema = get_schema(client)
    assert schema['paths']['/response/model-response']['get']['responses']['200']['content']['application/json']['schema']['$ref'] == '#/components/schemas/ModelDto'

def test_model_list_response_unified_style(app_setup):
    client = app_setup
    schema = get_schema(client)
    assert schema['paths']['/response/model-list-response']['get']['responses']['200']['content']['application/json']['schema']['type'] == 'array'
    assert schema['paths']['/response/model-list-response']['get']['responses']['200']['content']['application/json']['schema']['items']['$ref'] == '#/components/schemas/ModelDto'

def test_json_response_unified_style(app_setup):
    client = app_setup
    schema = get_schema(client)
    assert schema['paths']['/response/json-response']['get']['responses']['200']['content']['application/json']['schema']['type'] == 'object'

def test_plain_text_response_unified_style(app_setup):
    client = app_setup
    schema = get_schema(client)
    assert schema['paths']['/response/plain-text-response']['get']['responses']['200']['content']['text/plain']['schema']['type'] == 'string'

def test_html_response_unified_style(app_setup):
    client = app_setup
    schema = get_schema(client)
    assert schema['paths']['/response/html-response']['get']['responses']['200']['content']['text/html']['schema']['type'] == 'string'
    assert schema['paths']['/response/html-response']['get']['responses']['200']['content']['text/html']['schema']['format'] == 'html'

def test_empty_response_unified_style(app_setup):
    client = app_setup
    schema = get_schema(client)
    assert 'content' not in schema['paths']['/response/empty-response']['get']['responses']['200']
