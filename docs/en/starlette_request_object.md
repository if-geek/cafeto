# Request Object (Starlette)

## Introduction

In Starlette, the `request` object represents the HTTP request that arrives at an endpoint. It contains information such as the request methods (GET, POST, etc.), headers, path parameters, query string, request body, and more. It is essential for accessing and manipulating the incoming request data in your application.

The `Request` object from [Starlette](https://www.starlette.io/requests/) is not lost and can still be accessed from the controller.

## Usage

```python
from cafeto import Response
from cafeto.mvc import BaseController


@app.controller()
class HomeController(BaseController):
    @app.get('/hello')
    async def hello(self) -> Response:
        print(self.request)  # Request object
        return Response()
```

If the action is a websocket, you should use:

```python
from cafeto import Response
from cafeto.mvc import BaseController


@app.controller()
class HomeController(BaseController):
    @app.websocket('/ws')
    async def hello(self) -> Response:
        print(self.websocket)  # Request object
        return Response()
```
