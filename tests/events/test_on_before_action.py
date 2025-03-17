import pytest

from cafeto import App
from cafeto.events import OnBeforeAction
from cafeto.responses.unified_response import NoContent
from cafeto.testclient import TestClient
from cafeto.mvc import BaseController
from cafeto.mvc.types import Action


controller_name: str = None
action_name: str = None
path: str = None
method: str = None


@pytest.fixture(autouse=True)
def app_setup():
    app: App = App()

    def on_before_action(controller: BaseController, action: Action) -> None:
        global controller_name
        global action_name
        global path
        global method

        controller_name = controller.__class__.__name__
        action_name = action.__name__
        path = action.endpoint.path
        method = action.endpoint.method

    @app.controller()
    class HomeController(BaseController):
        @app.get('/home')
        async def home(self) -> None:
            return NoContent()

    app.map_controllers()

    OnBeforeAction.add(on_before_action)

    yield TestClient(app)


def test_on_before_action(app_setup):
    global controller_name
    global action_name
    global path
    global method
    
    client = app_setup
    response = client.get(f'/home/home')
    assert response.status_code == 204
    assert controller_name == 'HomeController'
    assert action_name == 'home'
    assert path == '/home/home'
    assert method == 'GET'
