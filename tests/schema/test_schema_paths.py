import pytest
from cafeto import App
from cafeto.testclient import TestClient
from cafeto.responses import NoContent
from cafeto.mvc import BaseController


@pytest.fixture(autouse=True)
def app_setup():
    app: App = App()

    @app.controller()
    class SchemaController(BaseController):
        @app.get('/get/{id}')
        async def get(self, id: int) -> None:
            return NoContent()

        @app.get('/get-all')
        async def get_all(self) -> None:
            return NoContent()

        @app.post('/create')
        async def create(self) -> None:
            return NoContent()

        @app.put('/update/{id}')
        async def update(self, id: int) -> None:
            return NoContent()

        @app.patch('/update-partial/{id}')
        async def update_partial(self) -> None:
            return NoContent()

        @app.delete('/delete/{id}')
        async def delete(self, id: int) -> None:
            return NoContent()


    app.map_controllers()
    app.use_schema()
    app.use_swagger()

    yield TestClient(app)

def get_schema(client):
    response = client.get('/schema/openapi.json')
    return response.json()

def test_paths(app_setup):
    client = app_setup
    schema = get_schema(client)
    assert len(schema['paths']) == 6
    assert '/schema/get/{id}' in schema['paths']
    assert '/schema/get-all' in schema['paths']
    assert '/schema/create' in schema['paths']
    assert '/schema/update/{id}' in schema['paths']
    assert '/schema/update-partial/{id}' in schema['paths']
    assert '/schema/delete/{id}' in schema['paths']
