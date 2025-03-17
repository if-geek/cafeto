from typing import List

import pytest

from cafeto import App
from cafeto.testclient import TestClient
from cafeto.responses import JSONResponse, PlainTextResponse, HTMLResponse, ModelResponse, Response
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
            return ModelResponse(ModelDto(**generate_model_data(1)))

        @app.get('/model-list-response')
        async def model_list_response(self) -> List[ModelDto]:
            return ModelResponse([
                ModelDto(**generate_model_data(1)),
                ModelDto(**generate_model_data(2))
            ])

        @app.get('/json-response')
        async def json_response(self) -> JSONResponse:
            return JSONResponse(generate_model_data(1))

        @app.get('/plain-text-response')
        async def plain_text_response(self) -> PlainTextResponse:
            return PlainTextResponse('Hello, World!')

        @app.get('/html-response')
        async def html_response(self) -> HTMLResponse:
            return HTMLResponse('<div>Hello, World!</div>')

        @app.get('/empty-response')
        async def empty_response(self) -> None:
            return Response()


    app.map_controllers()
    app.use_schema()
    app.use_swagger()

    yield TestClient(app)

def get_schema(client):
    response = client.get('/schema/openapi.json')
    return response.json()

def test_model_response_classic_style(app_setup):
    client = app_setup
    schema = get_schema(client)
    assert schema['paths']['/response/model-response']['get']['responses']['200']['content']['application/json']['schema']['$ref'] == '#/components/schemas/ModelDto'

def test_model_list_response_classic_style(app_setup):
    client = app_setup
    schema = get_schema(client)
    assert schema['paths']['/response/model-list-response']['get']['responses']['200']['content']['application/json']['schema']['type'] == 'array'
    assert schema['paths']['/response/model-list-response']['get']['responses']['200']['content']['application/json']['schema']['items']['$ref'] == '#/components/schemas/ModelDto'

def test_json_response_classic_style(app_setup):
    client = app_setup
    schema = get_schema(client)
    assert schema['paths']['/response/json-response']['get']['responses']['200']['content']['application/json']['schema']['type'] == 'object'

def test_plain_text_response_classic_style(app_setup):
    client = app_setup
    schema = get_schema(client)
    assert schema['paths']['/response/plain-text-response']['get']['responses']['200']['content']['text/plain']['schema']['type'] == 'string'

def test_html_response_classic_style(app_setup):
    client = app_setup
    schema = get_schema(client)
    assert schema['paths']['/response/html-response']['get']['responses']['200']['content']['text/html']['schema']['type'] == 'string'
    assert schema['paths']['/response/html-response']['get']['responses']['200']['content']['text/html']['schema']['format'] == 'html'

def test_empty_response_classic_style(app_setup):
    client = app_setup
    schema = get_schema(client)
    assert 'content' not in schema['paths']['/response/empty-response']['get']['responses']['200']
