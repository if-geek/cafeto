# Request

## Introducción

Un `request` en un servicio es una petición que un cliente envía a un servidor para que realice una operación específica. Esta petición incluye información clave, como el método HTTP (GET, POST, PUT, DELETE, etc.), la URL que identifica el recurso solicitado, los encabezados (headers) con datos contextuales (como autenticación o tipo de contenido) y, opcionalmente, un cuerpo (body) que contiene datos adicionales necesarios para procesar la solicitud, como formularios o JSON. El servidor procesa el request y devuelve una respuesta que indica el resultado de la operación.

Los `request` llegan a través de un DTO (Data Transfer Object). Es una manera de encapsular datos en un formato estructurado y tipado para garantizar que la información se transmita de manera consistente y segura.

## Uso

```python
from datetime import date
from typing import Optional

from cafeto import App
from cafeto.models import BaseModel
from cafeto.mvc import BaseController
from cafeto.responses import Ok


class ExtraDataRequestDto(BaseModel):
    nickname: str


class CreateUserRequestDto(BaseModel):
    username: str
    password: str
    confirm_password: str
    name: Optional[str]
    birth_date: date
    extra_data: ExtraDataRequestDto

app: App = App()

@app.controller('/user')
class UserController(BaseController):
    @app.post('/create')
    async def create(self, user: CreateUserRequestDto) -> Dict[str, Any]: #(1)
        return Ok({
            'username': user.username,
            'password': user.password,
            'name': user.name,
            'birth_date': user.birth_date,
            'extra_data': {
                'nickname': user.extra_data.nickname
            }
        })

app.map_controllers()
```

1. Aquí se recibe el objeto `CreateUserRequestDto`.
```python
    async def create(self, user: CreateUserRequestDto)
```

Para este ejemplo, solo se deben mapear los campos de la clase `CreateUserRequestDto`, incluyendo la clase `ExtraDataRequestDto` en un JSON así:

```sh
curl -X POST http://127.0.0.1:8000/user/create \
     -H "Content-Type: application/json" \
     -d '{
           "username": "jon-d",
           "password": "my-password-123",
           "confirm_password": "my-password-123",
           "name": "Jon Doe",
           "birth_date": "1984-01-01",
           "extra_data": {
            "nickname": "Jon"
           }
         }'
```

## Cargar archivos

Es posible crear una acción para cargar archivos. Para esto, se requiere que el request sea del tipo `UploadFile`.

```python
from cafeto import App
from cafeto.datastructures import UploadFile
from cafeto.models import BaseModel
from cafeto.mvc import BaseController
from cafeto.responses import Ok


@app.controller()
class StorageController(BaseController):
    @app.post('/upload')
    async def upload(self, file: UploadFile) -> Ok:
        return Ok({'file': file.filename})
```

El API se podrá consumir así:

```sh
curl -X POST http://127.0.0.1:8000/upload \
     -F "file=@path/to/your/file"
```
