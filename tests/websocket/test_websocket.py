import time

import json
from typing import List

import pytest

from cafeto import App
from cafeto.testclient import TestClient
from cafeto.background import BackgroundTask
from cafeto.responses import Ok, NoContent
from cafeto.mvc import BaseController

from tests.data import ChaDataRequestDto, ChaDataResponseDto


background_task_status: bool = False


@pytest.fixture(autouse=True)
def app_setup():
    app: App = App()

    @app.controller()
    class ChatController(BaseController):
        @app.websocket('/ws-chat-model')
        async def ws_chat_model(self) -> None:
            async def on_connect():
                pass

            async def on_disconnect():
                pass

            async def on_receive(data: ChaDataRequestDto) -> ChaDataResponseDto:
                return Ok(ChaDataResponseDto(message=f'Hi! {data.user}', user='System'))
                
            await self.websocket.accept_callback(
                on_connect=on_connect,
                on_disconnect=on_disconnect,
                on_receive=on_receive
            )

        @app.websocket('/ws-chat-list-model')
        async def ws_chat_list_model(self) -> None:
            async def on_connect():
                pass

            async def on_disconnect():
                pass

            async def on_receive(data: ChaDataRequestDto) -> List[ChaDataResponseDto]:
                return Ok([ChaDataResponseDto(message=f'Hi! {data.user} ({i})', user='System') for i in range(3)])
                
            await self.websocket.accept_callback(
                on_connect=on_connect,
                on_disconnect=on_disconnect,
                on_receive=on_receive
            )


        @app.websocket('/ws-chat-model-background-task')
        async def ws_chat_model_background_task(self) -> None:
            def background_task():
                global background_task_status
                background_task_status = True

            async def on_receive(data: ChaDataRequestDto) -> ChaDataResponseDto:
                global background_task_status
                background_task_status = False

                background_task_obj = BackgroundTask(background_task)
                return Ok(ChaDataResponseDto(message=f'Hi! {data.user}', user='System'), background=background_task_obj)
                
            await self.websocket.accept_callback(
                on_receive=on_receive
            )

        @app.websocket('/ws-chat-dict')
        async def ws_chat_dict(self) -> None:
            async def on_receive(data: ChaDataRequestDto) -> ChaDataResponseDto:
                return Ok({'message': f'Hi! {data.user}', 'user': 'System'})

            await self.websocket.accept_callback(
                on_receive=on_receive
            )

        @app.websocket('/ws-chat-no-content')
        async def ws_chat_no_content(self) -> None:
            async def on_receive(data: ChaDataRequestDto) -> ChaDataResponseDto:
                return NoContent()

            await self.websocket.accept_callback(
                on_receive=on_receive
            )
        
        @app.websocket('/ws-chat-model/response-other')
        async def ws_chat_model_response_other(self) -> None:
            async def on_receive(data: ChaDataRequestDto) -> None:
                await self.websocket.send_bytes(b'Nothing to see here')
                await self.websocket.close()
                
            await self.websocket.accept_callback(
                on_receive=on_receive
            )


        @app.websocket('/ws-chat-standar')
        async def ws_chat_standar(self) -> None:
            await self.websocket.accept()

            while True:
                try:
                    data = await self.websocket.receive_json()
                    request_model = ChaDataRequestDto.create(data)
                    # Do something with the request_model

                    response_model = ChaDataResponseDto.create({"message": 'Hi!', "user": 'System'})
                    # Do something with the response_model
                    await self.websocket.send_bytes(json.dumps({'message': f'Hi! {data["user"]}', 'user': 'System'}).encode('utf-8'))
                except Exception as e:
                    break


    @app.controller()
    class ChatStyle2Controller(BaseController):
        @app.websocket('/ws-chat-model')
        async def ws_chat_model(self) -> None:
            await self.websocket.accept_callback(
                on_connect=self.on_connect,
                on_disconnect=self.on_disconnect,
                on_receive=self.on_receive
            )

        async def on_connect(self):
            pass

        async def on_disconnect(self):
            pass

        async def on_receive(self, data: ChaDataRequestDto) -> ChaDataResponseDto:
            return Ok(ChaDataResponseDto(message=f'Hi! {data.user}', user='System'))

    app.map_controllers()
    yield TestClient(app)


def test_ws_model(app_setup):
    client = app_setup
    user = 'User # {}'
    response = client.websocket_connect('/chat/ws-chat-model')
    with response as ws:
        for i in range(4):
            ws.send_json({'message': 'Hola!!', 'user': user.format(i)})
            data = ws.receive_bytes()
            data = json.loads(data.decode('utf-8'))
            assert data == {
                'statusCode': 200,
                'body': {'message':f'Hi! {user.format(i)}', 'user':'System'}
            }


def test_ws_list_model(app_setup):
    client = app_setup
    user = 'User'
    response = client.websocket_connect('/chat/ws-chat-list-model')
    with response as ws:
        ws.send_json({'message': 'Hola!!', 'user': user})
        data = ws.receive_bytes()
        data = json.loads(data.decode('utf-8'))
        assert data == {
            'statusCode': 200,
            'body': [
                {'message':f'Hi! {user} (0)', 'user':'System'},
                {'message':f'Hi! {user} (1)', 'user':'System'},
                {'message':f'Hi! {user} (2)', 'user':'System'}
            ]
        }


def test_ws_model_background_task(app_setup):
    global background_task_status

    client = app_setup
    user = 'User'
    response = client.websocket_connect('/chat/ws-chat-model-background-task')
    with response as ws:
        ws.send_json({'message': 'Hola!!', 'user': user})
        data = ws.receive_bytes()
        data = json.loads(data.decode('utf-8'))
        assert data == {
            'statusCode': 200,
            'body': {'message':f'Hi! {user}', 'user':'System'}
        }
        time.sleep(0.1)
        assert background_task_status == True


def test_ws_dict(app_setup):
    global background_task_status

    client = app_setup
    user = 'User'
    response = client.websocket_connect('/chat/ws-chat-dict')
    with response as ws:
        ws.send_json({'message': 'Hola!!', 'user': user})
        data = ws.receive_bytes()
        data = json.loads(data.decode('utf-8'))
        assert data == {
            'statusCode': 200,
            'body': {'message':f'Hi! {user}', 'user':'System'}
        }


def test_ws_no_content(app_setup):
    global background_task_status

    client = app_setup
    user = 'User'
    response = client.websocket_connect('/chat/ws-chat-no-content')
    with response as ws:
        ws.send_json({'message': 'Hola!!', 'user': user})
        data = ws.receive_bytes()
        data = json.loads(data.decode('utf-8'))
        assert data['body'] == None


def test_ws_model_data_validation(app_setup):
    client = app_setup
    user = 'Marcela'
    response = client.websocket_connect('/chat/ws-chat-model')
    with response as ws:
        ws.send_json({'user': user})
        data = ws.receive_bytes()
        data = json.loads(data.decode('utf-8'))
        assert data == {
            'statusCode': 400,
            'body': {
                'errorList': [{
                    'type': 'missing',
                    'loc': ['message'],
                    'msg': 'Field required'
                }]
            }
        }

def test_ws_standar(app_setup):
    client = app_setup
    user = 'Stefania'
    response = client.websocket_connect('/chat/ws-chat-standar')
    with response as ws:
        ws.send_json({'message': 'Hola!!', 'user': user})
        data = ws.receive_bytes()
        data = json.loads(data.decode('utf-8'))
        assert data == {'message':f'Hi! {user}', 'user':'System'}

def test_ws_model_response_other(app_setup):
    client = app_setup
    user = 'John Doe'
    response = client.websocket_connect('/chat/ws-chat-model/response-other')
    with response as ws:
        ws.send_json({'message': 'Hola!!', 'user': user})
        data = ws.receive_bytes()
        assert data == b'Nothing to see here'

def test_ws_style_2_model(app_setup):
    client = app_setup
    user = 'Rocio'
    response = client.websocket_connect('/chatstyle2/ws-chat-model')
    with response as ws:
        ws.send_json({'message': 'Hola!!', 'user': user})
        data = ws.receive_bytes()
        data = json.loads(data.decode('utf-8'))
        assert data == {
            'statusCode': 200,
            'body': {'message':f'Hi! {user}', 'user':'System'}
        }
