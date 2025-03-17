import pytest
from cafeto import App
from cafeto.testclient import TestClient
from cafeto.responses import NoContent
from cafeto.mvc import BaseController
from cafeto.schema import Contact, Info, License


@pytest.fixture(autouse=True)
def app_setup():
    app: App = App()

    @app.controller()
    class SchemaController(BaseController):
        @app.get('/get')
        async def get(self) -> None:
            return NoContent()

    app.map_controllers()
    app.use_schema(
        openapi_version = '3.0.1',
        info = Info(
            title = 'Test',
            version = '1.0.0',
            description = 'Test description',
            terms_of_service = 'http://example.com/terms',
            contact = Contact(
                name = 'Test',
                url='http://example.com',
                email = 'example@example.com'
            ),
            license = License(
                name = 'Apache 2.0',
                url = 'http://www.apache.org/licenses/LICENSE-2.0'
            )
        )
    )
    app.use_swagger()

    yield TestClient(app)


def get_schema(client):
    response = client.get('/schema/openapi.json')
    return response.json()

def test_info(app_setup):
    client = app_setup
    schema = get_schema(client)
    assert schema['openapi'] == '3.0.1'
    assert schema['info'] == {
        'title': 'Test',
        'version': '1.0.0',
        'description': 'Test description',
        'termsOfService': 'http://example.com/terms',
        'contact': {
            'name': 'Test',
            'url': 'http://example.com',
            'email': 'example@example.com'
        },
        'license': {
            'name': 'Apache 2.0',
            'url': 'http://www.apache.org/licenses/LICENSE-2.0'
        }
    }
