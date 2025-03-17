# WebSockets

## Introduction

WebSockets are a technology that allows real-time bidirectional communication between a client (such as a web browser) and a server. This is done through a single persistent socket connection, which reduces latency and improves efficiency in applications that need frequent updates, such as live chats, online games, or real-time dashboards.

Cafeto uses the same WebSockets from Starlette for real-time communication and offers two ways to implement it.

## Traditional Method

```python
@app.controller()
class WsController(BaseController):
    @app.websocket('/chat')
    async def chat(self) -> None:
        await self.websocket.accept()
        # Your code on connect here.

        while True:
            try:
                # Your code on receive here.
                data = await self.websocket.receive_json()

                # Send message.
                await self.websocket.send_json({'Hola': 'Mundo'})
            except Exception as e:
                # Your code on disconnect here.
                break
```

In this case, the information is received as JSON without being assigned to a DTO, and the response is a JSON with the format:

```json
{
    "message": "Hi",
    "user": "System"
}
```

## Callback Method

=== "Unified Style"

    ```python
    from cafeto.mvc import BaseController
    from cafeto.responses import Ok

    @app.controller()
    class WsController(BaseController):
        @app.websocket('/chat')
        async def chat(self) -> None:
            async def on_connect():
                pass # Your code on connect here.

            async def on_disconnect():
                pass # Your code on disconnect here.

            async def on_receive(data: ChatRequestDto) -> ChatResponseDto:
                # Your code on receive here.
                response = ChatResponseDto(message='Hi', user='System')

                # Response message.
                return Ok(response)
                
            await self.websocket.accept_callback(
                on_connect=on_connect,
                on_disconnect=on_disconnect,
                on_receive=on_receive
            )
    ```

=== "Classic Style"

    ```python
    from cafeto.mvc import BaseController
    from cafeto.responses import ModelWSResponse

    @app.controller()
    class WsController(BaseController):
        @app.websocket('/chat')
        async def chat(self) -> None:
            async def on_connect():
                pass # Your code on connect here.

            async def on_disconnect():
                pass # Your code on disconnect here.

            async def on_receive(data: ChatRequestDto) -> ChatResponseDto:
                # Your code on receive here.
                response = ChatResponseDto(message='Hi', user='System')

                # Response message.
                return ModelWSResponse(response)
                
            await self.websocket.accept_callback(
                on_connect=on_connect,
                on_disconnect=on_disconnect,
                on_receive=on_receive
            )
    ```

    > **Note**: It is important to note that the response should not be made using `ModelResponse` but `ModelWSResponse`.
    For now, responses like JSONResponse, PlainTextResponse, and HTMLResponse are not available with WebSockets.

It is also possible to do it this way:

=== "Unified Style"

    ```python
    from cafeto.mvc import BaseController
    from cafeto.responses import Ok

    @app.controller()
    class WsController(BaseController):
        @app.websocket('/chat')
        async def chat(self) -> None:
            await self.websocket.accept_callback(
                on_receive=self.on_receive,
                on_connect=self.on_connect,
                on_disconnect=self.on_disconnect
            )
        
        async def on_connect(self):
            pass # Your code on connect here.

        async def on_disconnect(self) -> None:
            pass # Your code on disconnect here.

        async def on_receive(self, data: ChatRequestDto) -> ChatResponseDto:
            # Your code on receive here.
            response = ChatResponseDto(message='Hi', user='System')

            # Response message.
            return Ok(response)
    ```

=== "Classic Style"

    ```python
    from cafeto.mvc import BaseController
    from cafeto.responses import ModelWSResponse

    @app.controller()
    class WsController(BaseController):
        @app.websocket('/chat')
        async def chat(self) -> None:
            await self.websocket.accept_callback(
                on_receive=self.on_receive,
                on_connect=self.on_connect,
                on_disconnect=self.on_disconnect
            )
        
        async def on_connect(self):
            pass # Your code on connect here.

        async def on_disconnect(self) -> None:
            pass # Your code on disconnect here.

        async def on_receive(self, data: ChatRequestDto) -> ChatResponseDto:
            # Your code on receive here.
            response = ChatResponseDto(message='Hi', user='System')

            # Response message.
            return ModelWSResponse(response)
    ```

In this method, messages arrive in a DTO, with all the validations and features that DTOs imply in HTTP actions.

The response also changes, as WebSocket messages do not have a `statusCode` like traditional HTTP requests. The incoming message would have the following format:

```json
{
    "statusCode": 200,
    "body": {
        "message": "Hi",
        "user": "System"
    }
}
```

But if the DTO validations fail, the response could be:

```json
{
    "statusCode": 400,
    "body": {
        "errorList": [
            {
                "loc": ["message"],
                "type": "missing",
                "msg": "Field required"
            }
        ]
    }
}
```

In this way, the response of HTTP requests can be emulated.

> **Note**: Only the `on_receive` callback is required; `on_connect` and `on_disconnect` are optional.
