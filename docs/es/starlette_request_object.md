# Objeto Request (Starlette)

## Introducción

En Starlette, el objeto `request` representa la solicitud HTTP que llega a un endpoint. Contiene información como los métodos de la solicitud (GET, POST, etc.), encabezados, parámetros de ruta, cadena de consulta, cuerpo de la solicitud y más. Es esencial para acceder y manipular los datos de la solicitud entrante en tu aplicación.

El objeto `Request` de [Starlette](https://www.starlette.io/requests/) no se pierde y aún puede ser accedido desde el controlador.

## Uso

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

En caso de que la acción sea un websocket se debe usar:

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
