# Parameters

## Introduction

Parameters in an API are key elements that allow customizing requests and responses. They are divided into three main types:

**Path Parameters**

:   Define variable parts of the URL.

    **Importance**: Allow direct and structured access to specific resources.

**Query String Parameters**
:   Are added to the URL after the `?` symbol and are separated by `&`.

    **Importance**: Facilitate filtering, sorting, and customizing results without modifying the path.

**Headers**

:   Are sent as part of the HTTP request.

    **Importance**: Provide metadata about the request, such as authentication, content format, and more.

These parameters are essential for the flexibility, security, and efficiency of communication between the client and the server in an API.

## Path Parameters

It is possible to obtain parameters in the URL as done in [Starlette](https://www.starlette.io/routing/), but they will be obtained as a parameter in the action.

```python
from typing import Dict

from cafeto.mvc import BaseController
from cafeto.responses import Ok


@app.controller()
class ParamsController(BaseController):
    @app.get('/get-params/{id}')
    async def get_params(self, id: int) -> Dict[str, int]:
        return Ok({'id': id})
```

The API can be consumed like this:

```bash
curl -X GET http://127.0.0.1:8000/params/get-params/1 \
     -H "Content-Type: application/json"
```

> **Note**: Unlike Starlette, the parameter type is not defined in the URL but in the action parameter:

!!! danger
    **Incorrect way**

    ```python
    @app.get('/get-params/{id:int}')
    async def get_params(self, id):
        ...
    ```

!!! success
    **Correct way**

    ```python
    @app.get('/get-params/{id}')
    async def get_params(self, id: int):
        ...
    ``` 

These parameters are mandatory and can be defined as many as needed.

```python
from typing import Dict, Any

from cafeto.mvc import BaseController
from cafeto.responses import Ok


@app.controller()
class ParamsController(BaseController):
    @app.get('/get-params/{id}/{group}')
    async def get_params(self, id: int, group: str) -> Dict[str, Any]:
        return Ok({'id': id, 'group': group})
```

The API can be consumed like this:

```bash
curl -X GET http://127.0.0.1:8000/params/get-params/1/employee \
     -H "Content-Type: application/json"
```

## Query String Parameters

It is possible to obtain parameters from the query string like this:

```python
from typing import Dict

from cafeto.mvc import BaseController
from cafeto.responses import Ok


@app.controller()
class ParamsController(BaseController):
    @app.get('/get-params', query=['group'])
    async def get_params(self, group: str) -> Dict[str, str]:
        return Ok({'group': group})
```

The API can be consumed like this:

```bash
curl -X GET http://127.0.0.1:8000/params/get-params?group=employee \
     -H "Content-Type: application/json" 
```

## Header Parameters

It is possible to obtain parameters from the headers like this:

```python
from typing import Dict

from cafeto.mvc import BaseController
from cafeto.responses import Ok


@app.controller()
class ParamsController(BaseController):
    @app.get('/get-params', headers=['token'])
    async def get_params(self, token: str) -> Dict[str, str]:
        return Ok({'token': token})
```

The API can be consumed like this:

```bash
curl -X GET http://127.0.0.1:8000/params/get-params \
     -H "Content-Type: application/json" \
     -H "token: token123" 
```

It is possible to obtain multiple parameters from the three different sources like this:

```python
from typing import Dict, Any

from cafeto.mvc import BaseController
from cafeto.responses import Ok


@app.controller()
class ParamsController(BaseController):
    @app.get(
        '/get-params/{id}/{group}',
        query=['confirm'],
        headers=['token', 'language'])
    async def get_params(
        self,
        id: int,
        token: str,
        confirm: int,
        group: str,
        language: str) -> Dict[str, Any]:
        return Ok({
            'id': id,
            'token': token,
            'confirm': confirm,
            'group': group,
            'language': language
        })
```

The API can be consumed like this:

```bash
curl -X GET http://127.0.0.1:8000/params/get-params/1/employee?confirm=1 \
     -H "Content-Type: application/json" \
     -H "token: token123" \
     -H "language: esCO" 
```

As seen in the previous example, the order of the parameters does not really matter.

`Header` and `query string` parameters can have default values. This means that if the parameter is not found, the default value assigned in the action definition will be used.

```python
from typing import Dict

from cafeto.mvc import BaseController
from cafeto.responses import Ok


@app.controller()
class ParamsController(BaseController):
    @app.get('/create', query=['group'])
    async def create(self, group: str='employee') -> Dict[str, str]:
        return Ok({'group': group})
```

In this last example, `group` has a default value, so it must be at the end of the parameters and this value will be used if the parameter is not found in the `query string`.
