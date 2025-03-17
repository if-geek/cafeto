# Respuestas

## Introducción

La respuesta de un servicio es el resultado que se envía al cliente tras procesar una solicitud. Puede tener diferentes formatos dependiendo de la necesidad, como JSON para datos estructurados, texto plano para mensajes simples, HTML para contenido web, archivos binarios para descargas o incluso respuestas en streaming para datos enviados progresivamente. Su contenido y código de estado (como 200 para éxito o 400 para errores) indican el resultado de la operación realizada.

En sus acciones, Cafeto utiliza las respuestas estándar de `Starlette`, que incluyen: `JSON`, `HTML`, `Texto Plano`, `Archivos Binarios`, `Streaming` o `None` (sin contenido). Además, Cafeto ofrece dos respuestas adicionales para manejar DTOs: `ModelResponse` y `ModelWSResponse` (específica para websockets). Este enfoque lo llamamos el `Método Clásico`.

Complementando las respuestas del `Método Clásico`, Cafeto introduce un sistema adicional denominado `Método Unificado`. 

La principal diferencia es que en el `Método Clásico` el desarrollador debe elegir manualmente el tipo de respuesta según el dato a retornar. En contraste, el `Método Unificado` siempre utiliza una única respuesta que puede detectar automáticamente el tipo de dato a retornar, simplificando el proceso.

En el `Método Clásico`, el código de estado por defecto (`statusCode`) es siempre `200`, y debe ajustarse manualmente según las necesidades. Por otro lado, en el `Método Unificado`, cada tipo de respuesta está asociado automáticamente a un código de estado específico.


=== "Estilo Unificado"

    - Ok (Respuesta con código 200)
    - BadRequest (Respuesta con código 400)
    - NoContent (Respuesta con código 204)
    - ETC...

=== "Estilo Clásico"

    - Response (Respuesta sin contenido)
    - JSONResponse (Respuesta de un JSON)
    - PlainTextResponse (Respuesta de texto plano)
    - HTMLResponse (Respuesta de texto con formato HTML)
    - FileResponse (Respuesta de un archivo binario)
    - StreamingResponse (Respuesta en forma de streaming)
    - ModelResponse (Respuesta de un modelo)
    - ModelWSResponse (Respuesta de un modelo, pero desde un websocket)

## Respuesta JSON

=== "Estilo Unificado"

    ```python
    from cafeto.responses import Ok

    @app.controller()
    class UserController:
        @app.get('/view')
        async def view(self) -> Dict[str, str]:
            return Ok({'Hello': 'Hola'})
    ```

=== "Estilo Clásico"

    ```python
    from cafeto.responses import JSONResponse

    @app.controller()
    class UserController:
        @app.get('/view')
        async def view(self) -> JSONResponse:
            return JSONResponse({'Hello': 'Hola'})
    ```

Es importante recordar que el tipo de respuesta de las acciones no es estrictamente obligatorio y solo se usa para la documentación con OpenApi, pero se sugiere usarla para tener un proyecto más claro y fácil de mantener.

=== "Estilo Unificado"

    ```python
    from cafeto.responses import Ok

    @app.controller()
    class UserController:
        @app.get('/view')
        async def view(self):  # No response
            return Ok({'Hello': 'Hola'})
    ```

=== "Estilo Clásico"

    ```python
    from cafeto.responses import JSONResponse

    @app.controller()
    class UserController:
        @app.get('/view')
        async def view(self):  # No response
            return JSONResponse({'Hello': 'Hola'})
    ```

## Respuesta DTO

=== "Estilo Unificado"

    ```python
    from cafeto.responses import Ok

    @app.controller()
    class UserController:
        @app.get('/view')
        async def view(self) -> CreateUserResponseDto:
            user = <some_user_service>.get() #(1)
            return Ok(CreateUserResponseDto(**user)) #(2)
    ```

    1. !!! warning
       Servicio simulado para el ejemplo.

    2. Aquí se envía el objeto `CreateUserResponseDto`

=== "Estilo Clásico"

    ```python
    from cafeto.responses import ModelResponse

    @app.controller()
    class UserController:
        @app.get('/view')
        async def view(self) -> CreateUserResponseDto:
            user = <some_user_service>.get() #(1)
            return ModelResponse(CreateUserResponseDto(**user)) #(2)
    ```

    1. !!! warning
       Servicio simulado para el ejemplo.

    2. Aquí se envía el objeto `CreateUserResponseDto`

## Respuesta Lista de DTOs

=== "Estilo Unificado"

    ```python
    from cafeto.responses import Ok

    @app.controller()
    class UserController:
        @app.get('/view')
        async def view(self) -> List[CreateUserResponseDto]:
            users = <some_user_service>.get_all()
            return Ok(
                [CreateUserResponseDto(**user) for user in users]
            )
    ```

=== "Estilo Clásico"

    ```python
    from cafeto.responses import ModelResponse

    @app.controller()
    class UserController:
        @app.get('/view')
        async def view(self) -> List[CreateUserResponseDto]:
            users = <some_user_service>.get_all()
            return ModelResponse(
                [CreateUserResponseDto(**user) for user in users]
            )
    ```

## Respuesta sin contenido

=== "Estilo Unificado"

    ```python
    from cafeto.responses import NoContent

    @app.controller()
    class UserController:
        @app.post('/check')
        async def check(self) -> None:
            return NoContent()
    ```

=== "Estilo Clásico"

    ```python
    from cafeto.responses import Response

    @app.controller()
    class UserController:
        @app.post('/check')
        async def check(self) -> Response:
            return Response()
    ```

## Respuesta archivo o binario

=== "Estilo Unificado"

    ```python
    from cafeto.responses import Ok, FileResponse

    @app.controller()
    class UserController:
        @app.get('/check')
        async def check(self) -> FileResponse:
            return Ok(FileResponse('/path/to/file'))
    ```

=== "Estilo Clásico"

    ```python
    from cafeto.responses import FileResponse

    @app.controller()
    class UserController:
        @app.get('/check')
        async def check(self) -> FileResponse:
            return FileResponse('/path/to/file')
    ```

## Respuesta texto plano

=== "Estilo Unificado"

    ```python
    from cafeto.responses import Ok

    @app.controller()
    class UserController:
        @app.get('/check')
        async def check(self) -> str:
            return Ok('Hello World!')
    ```

=== "Estilo Clásico"

    ```python
    from cafeto.responses import PlainTextResponse

    @app.controller()
    class UserController:
        @app.get('/check')
        async def check(self) -> PlainTextResponse:
            return PlainTextResponse('Hello World!')
    ```

## Respuesta HTML

=== "Estilo Unificado"

    ```python
    from cafeto.responses import Ok, Format
    from cafeto.responses.types import TEXT_HTML

    @app.controller()
    class UserController:
        @app.get('/check')
        async def check(self) -> Format[str, TEXT_HTML]:
            return Ok('<div>Hello World!</div>', format=TEXT_HTML)
    ```

=== "Estilo Clásico"

    ```python
    from cafeto.responses import HTMLResponse

    @app.controller()
    class UserController:
        @app.get('/check')
        async def check(self) -> HTMLResponse:
            return HTMLResponse('<div>Hello World!</div>')
    ```

## Respuesta Streaming

=== "Estilo Unificado"

    ```python
    from cafeto.responses import Ok, Format
    from cafeto.responses.types import TEXT_HTML

    async def slow_numbers(minimum, maximum):
        yield '<ul>'
        for number in range(minimum, maximum + 1):
            yield f'<li>{number}</li>'
            await asyncio.sleep(0.5)
        yield '</ul>'

    @app.controller()
    class UserController:
        @app.get('/check')
        async def check(self) -> Format[str, TEXT_HTML]:
            generator = slow_numbers(1, 10)
            return Ok(generator, format=TEXT_HTML)
    ```

=== "Estilo Clásico"

    ```python
    from cafeto.responses import StreamingResponse

    async def slow_numbers(minimum, maximum):
        yield '<ul>'
        for number in range(minimum, maximum + 1):
            yield f'<li>{number}</li>'
            await asyncio.sleep(0.5)
        yield '</ul>'

    @app.controller()
    class UserController:
        @app.get('/check')
        async def check(self) -> HTMLResponse:
            generator = slow_numbers(1, 10)
            return StreamingResponse(generator)
    ```

## Conclusión

Ambos sistemas son bastante buenos, cada uno tiene sus pros y sus contras. Queda a discreción de cada desarrollador usar uno u otro. Se recomienda elegir uno desde el comienzo para evitar la confusión y no combinar los dos sistemas, así se tendrá mayor orden y control sobre el sistema.