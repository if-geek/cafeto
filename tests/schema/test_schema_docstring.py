import pytest
from cafeto import App
from cafeto.testclient import TestClient
from cafeto.responses import Ok
from cafeto.mvc import BaseController
from cafeto.schema import DefaultDocs, ExternalDocs, SecurityScheme

from tests.data import ModelDto, generate_model_data


@pytest.fixture(autouse=True)
def app_setup():
    app: App = App()

    @app.controller()
    class DocstringController(BaseController):
        '''
        description: This is a description for the controller
        '''
        @app.put('/update/{id}')
        async def update(self, id: int, data: ModelDto) -> ModelDto:
            '''
            summary: This is a summary for the action
            description: This is a description for the action
            responses:
                200:
                    default: true
                    description: Custom successful response
                400:
                    description: Custom bad response
            '''
            return Ok(ModelDto(generate_model_data(1)))


    @app.controller()
    class NoDocstringController(BaseController):
        @app.put('/update/{id}')
        async def update(self, id: int, data: ModelDto) -> ModelDto:
            return Ok(ModelDto(generate_model_data(1)))

    app.map_controllers()
    app.use_schema(
        external_docs=ExternalDocs(url='https://127.0.0.1', description='Schema documentation'),
        security_scheme=SecurityScheme(name='appAuth', type='apiKey', in_='header', bearer_format='JWT')
    )
    app.use_swagger()


    yield TestClient(app)

def get_schema(client):
    response = client.get('/schema/openapi.json')
    return response.json()

def test_docstring(app_setup):
    client = app_setup
    schema = get_schema(client)
    assert len(schema['paths']['/docstring/update/{id}']['put']['responses']) == 2
    assert schema['tags'][0]['name'] == 'DocstringController'
    assert schema['tags'][0]['description'] == 'This is a description for the controller'
    assert schema['paths']['/docstring/update/{id}']['put']['summary'] == 'This is a summary for the action'
    assert schema['paths']['/docstring/update/{id}']['put']['description'] == 'This is a description for the action'
    assert schema['paths']['/docstring/update/{id}']['put']['responses']['200']['description'] == 'Custom successful response'
    assert schema['paths']['/docstring/update/{id}']['put']['responses']['400']['description'] == 'Custom bad response'

def test_no_docstring(app_setup):
    client = app_setup
    schema = get_schema(client)
    assert len(schema['paths']['/nodocstring/update/{id}']['put']['responses']) == 1
    assert schema['tags'][1]['name'] == 'NoDocstringController'
    assert schema['tags'][1]['description'] == DefaultDocs.controller_description
    assert schema['paths']['/nodocstring/update/{id}']['put']['summary'] == DefaultDocs.action_summary
    assert schema['paths']['/nodocstring/update/{id}']['put']['description'] == DefaultDocs.action_description
    assert schema['paths']['/nodocstring/update/{id}']['put']['responses']['200']['description'] == DefaultDocs.action_description_response
