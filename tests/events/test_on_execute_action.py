import pytest

from cafeto import App
from cafeto.models.base_model import BaseModel
from cafeto.events import OnExecuteAction
from cafeto.responses.unified_response import NoContent
from cafeto.testclient import TestClient
from cafeto.mvc import BaseController
from cafeto.mvc.types import Action
from tests.data import ModelDto, assert_model, generate_extra_model_data


controller_name: str = None
action_name: str = None
path: str = None
method: str = None
request_model: BaseModel


@pytest.fixture(autouse=True)
def app_setup():
    app: App = App()

    def on_execute_action(controller: BaseController, action: Action, _request_model: BaseModel) -> None:
        global controller_name
        global action_name
        global path
        global method
        global request_model

        controller_name = controller.__class__.__name__
        action_name = action.__name__
        path = action.endpoint.path
        method = action.endpoint.method
        request_model = _request_model

    @app.controller()
    class HomeController(BaseController):
        @app.post('/home')
        async def home(self, request: ModelDto) -> None:
            return NoContent()

    app.map_controllers()

    OnExecuteAction.add(on_execute_action)

    yield TestClient(app)


def test_on_execute_action(app_setup):
    global controller_name
    global action_name
    global path
    global method
    global request_model

    seed: int = 1
    
    client = app_setup
    data = generate_extra_model_data(seed)
    response = client.post(f'/home/home', json=data)
    assert response.status_code == 204
    assert controller_name == 'HomeController'
    assert action_name == 'home'
    assert path == '/home/home'
    assert method == 'POST'
    assert_model(request_model.model_dump(mode='json') , seed)
