# Responses

## Introduction

The response of a service is the result sent to the client after processing a request. It can have different formats depending on the need, such as JSON for structured data, plain text for simple messages, HTML for web content, binary files for downloads, or even streaming responses for progressively sent data. Its content and status code (like 200 for success or 400 for errors) indicate the result of the operation performed.

In its actions, Cafeto uses the standard responses from `Starlette`, which include: `JSON`, `HTML`, `Plain Text`, `Binary Files`, `Streaming`, or `None` (no content). Additionally, Cafeto offers two extra responses to handle DTOs: `ModelResponse` and `ModelWSResponse` (specific for websockets). This approach is called the `Classic Method`.

Complementing the responses of the `Classic Method`, Cafeto introduces an additional system called the `Unified Method`.

The main difference is that in the `Classic Method`, the developer must manually choose the type of response according to the data to be returned. In contrast, the `Unified Method` always uses a single response that can automatically detect the type of data to be returned, simplifying the process.

In the `Classic Method`, the default status code (`statusCode`) is always `200`, and it must be adjusted manually according to the needs. On the other hand, in the `Unified Method`, each type of response is automatically associated with a specific status code.

=== "Unified Style"

    - Ok (Response with status code 200)
    - BadRequest (Response with status code 400)
    - NoContent (Response with status code 204)
    - ETC...

=== "Classic Style"

    - Response (No content response)
    - JSONResponse (JSON response)
    - PlainTextResponse (Plain text response)
    - HTMLResponse (HTML formatted text response)
    - FileResponse (Binary file response)
    - StreamingResponse (Streaming response)
    - ModelResponse (Model response)
    - ModelWSResponse (Model response, but from a websocket)

## JSON Response

=== "Unified Style"

    ```python
    from cafeto.responses import Ok

    @app.controller()
    class UserController:
        @app.get('/view')
        async def view(self) -> Dict[str, str]:
            return Ok({'Hello': 'Hola'})
    ```

=== "Classic Style"

    ```python
    from cafeto.responses import JSONResponse

    @app.controller()
    class UserController:
        @app.get('/view')
        async def view(self) -> JSONResponse:
            return JSONResponse({'Hello': 'Hola'})
    ```

It is important to remember that the response type of the actions is not strictly mandatory and is only used for documentation with OpenApi, but it is suggested to use it to have a clearer and easier to maintain project.

=== "Unified Style"

    ```python
    from cafeto.responses import Ok

    @app.controller()
    class UserController:
        @app.get('/view')
        async def view(self):  # No response
            return Ok({'Hello': 'Hola'})
    ```

=== "Classic Style"

    ```python
    from cafeto.responses import JSONResponse

    @app.controller()
    class UserController:
        @app.get('/view')
        async def view(self):  # No response
            return JSONResponse({'Hello': 'Hola'})
    ```

## DTO Response

=== "Unified Style"

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
       Simulated service for the example.

    2. Here the `CreateUserResponseDto` object is sent.

=== "Classic Style"

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
       Simulated service for the example.

    2. Here the `CreateUserResponseDto` object is sent.

## List of DTOs Response

=== "Unified Style"

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

=== "Classic Style"

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

## No Content Response

=== "Unified Style"

    ```python
    from cafeto.responses import NoContent

    @app.controller()
    class UserController:
        @app.post('/check')
        async def check(self) -> None:
            return NoContent()
    ```

=== "Classic Style"

    ```python
    from cafeto.responses import Response

    @app.controller()
    class UserController:
        @app.post('/check')
        async def check(self) -> Response:
            return Response()
    ```

## File or Binary Response

=== "Unified Style"

    ```python
    from cafeto.responses import Ok, FileResponse

    @app.controller()
    class UserController:
        @app.get('/check')
        async def check(self) -> FileResponse:
            return Ok(FileResponse('/path/to/file'))
    ```

=== "Classic Style"

    ```python
    from cafeto.responses import FileResponse

    @app.controller()
    class UserController:
        @app.get('/check')
        async def check(self) -> FileResponse:
            return FileResponse('/path/to/file')
    ```

## Plain Text Response

=== "Unified Style"

    ```python
    from cafeto.responses import Ok

    @app.controller()
    class UserController:
        @app.get('/check')
        async def check(self) -> str:
            return Ok('Hello World!')
    ```

=== "Classic Style"

    ```python
    from cafeto.responses import PlainTextResponse

    @app.controller()
    class UserController:
        @app.get('/check')
        async def check(self) -> PlainTextResponse:
            return PlainTextResponse('Hello World!')
    ```

## HTML Response

=== "Unified Style"

    ```python
    from cafeto.responses import Ok, Format
    from cafeto.responses.types import TEXT_HTML

    @app.controller()
    class UserController:
        @app.get('/check')
        async def check(self) -> Format[str, TEXT_HTML]:
            return Ok('<div>Hello World!</div>', format=TEXT_HTML)
    ```

=== "Classic Style"

    ```python
    from cafeto.responses import HTMLResponse

    @app.controller()
    class UserController:
        @app.get('/check')
        async def check(self) -> HTMLResponse:
            return HTMLResponse('<div>Hello World!</div>')
    ```

## Streaming Response

=== "Unified Style"

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

=== "Classic Style"

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

## Conclusion

Both systems are quite good, each with its pros and cons. It is up to each developer to use one or the other. It is recommended to choose one from the beginning to avoid confusion and not to combine the two systems, thus having greater order and control over the system.
