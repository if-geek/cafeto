# Parámetros

## Introducción

Los parámetros en una API son elementos clave que permiten personalizar las solicitudes y respuestas. Se dividen en tres tipos principales:

**Path Parameters (Parámetros de ruta)**

:   Definen partes variables de la URL.

    **Importancia**: Permiten acceder a recursos específicos de manera directa y estructurada.

**Query String Parameters (Parámetros de cadena de consulta)**

:   Se añaden a la URL después del símbolo `?` y están separados por `&`.

    **Importancia**: Facilitan la filtración, clasificación y personalización de los resultados sin modificar la ruta.

**Headers (Cabeceras)**

:   Se envían como parte de la solicitud HTTP.

    **Importancia**: Proporcionan metadatos sobre la solicitud, como autenticación, formato del contenido, entre otros.

Estos parámetros son esenciales para la flexibilidad, seguridad y eficiencia de la comunicación entre el cliente y el servidor en una API.

## Parámetros en la ruta (path)

Es posible obtener parámetros en la URL tal como se hace en [Starlette](https://www.starlette.io/routing/), pero se obtendrán como un parámetro en la acción.

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

El API se podrá consumir así:

```bash
curl -X GET http://127.0.0.1:8000/params/get-params/1 \
     -H "Content-Type: application/json"
```

> **Nota**: A diferencia de Starlette, el tipo del parámetro no se define en la URL, sino en el parámetro de la acción:

!!! danger
    **Forma incorrecta**

    ```python
    @app.get('/get-params/{id:int}')
    async def get_params(self, id):
        ...
    ```

!!! success
    **Forma correcta**

    ```python
    @app.get('/get-params/{id}')
    async def get_params(self, id: int):
        ...
    ``` 

Estos parámetros son obligatorios y se pueden definir cuantos sean necesarios.

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

El API se podrá consumir así:

```bash
curl -X GET http://127.0.0.1:8000/params/get-params/1/employee \
     -H "Content-Type: application/json"
```

## Parámetros en el query string

Es posible obtener parámetros desde query string así:

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

El API se podrá consumir así:

```bash
curl -X GET http://127.0.0.1:8000/params/get-params?group=employee \
     -H "Content-Type: application/json" 
```

## Parámetros en las cabeceras (headers)

Es posible obtener parámetros desde las cabeceras así:

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

El API se podrá consumir así:

```bash
curl -X GET http://127.0.0.1:8000/params/get-params \
     -H "Content-Type: application/json" \
     -H "token: token123" 
```

Es posible obtener varios datos de los parámetros de las tres diferentes fuentes así:

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

El API se podrá consumir así:

```bash
curl -X GET http://127.0.0.1:8000/params/get-params/1/employee?confirm=1 \
     -H "Content-Type: application/json" \
     -H "token: token123" \
     -H "language: esCO" 
```

Como se puede ver en el ejemplo anterior, el orden de los parámetros no importa realmente.

Los parámetros de las `cabeceras (headers)` y del `query string` pueden tener valores por defecto. Esto significa que si el parámetro no se encuentra, se usará el valor asignado por defecto en la definición de la acción.

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

Para este último ejemplo, `group` al tener un valor por defecto, debe estar al final de los parámetros y se usará este valor si el parámetro no se encuentra en el `query string`.
