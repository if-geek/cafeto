# WebSockets

## Introducción

Los WebSockets son una tecnología que permite la comunicación bidireccional en tiempo real entre un cliente (como un navegador web) y un servidor. Esto se realiza a través de una única conexión de socket persistente, lo que reduce la latencia y mejora la eficiencia en aplicaciones que necesitan actualizaciones frecuentes, como chats en vivo, juegos en línea o paneles de control en tiempo real.

Cafeto utiliza los mismos WebSockets de Starlette para la comunicación en tiempo real y ofrece dos formas de implementarlo.

## Método tradicional

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

En este caso, se recibe la información como un JSON sin ser asignado a un DTO y la respuesta es un JSON con el formato:

```json
{
    "message": "Hi",
    "user": "System"
}
```

## Método callback

=== "Estilo Unificado"

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

=== "Estilo Clásico"

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

    > **Nota**: Es importante notar que la respuesta no se debe hacer usando `ModelResponse` sino `ModelWSResponse`.
    Por ahora, las respuestas como JSONResponse, PlainTextResponse y HTMLResponse no están disponibles con WebSockets.

También es posible hacerlo así:

=== "Estilo Unificado"

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

=== "Estilo Clásico"

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

En este método, los mensajes llegan en un DTO, con todas las validaciones y características que los DTO implican en las acciones HTTP.

La respuesta también cambia, ya que los mensajes por WebSockets no tienen un `statusCode` como las peticiones HTTP tradicionales. El mensaje que llega tendría el siguiente formato:

```json
{
    "statusCode": 200,
    "body": {
        "message": "Hi",
        "user": "System"
    }
}
```

Pero si las validaciones del DTO fallan, la respuesta podría ser:

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

De esta forma, se puede emular la respuesta de las peticiones HTTP.

> **Nota**: Solo el callback `on_receive` es requerido; `on_connect` y `on_disconnect` son opcionales.