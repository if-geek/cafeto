# Request

## Introduction

A request in a service is a petition that a client sends to a server to perform a specific operation. This request includes key information such as the HTTP method (GET, POST, PUT, DELETE, etc.), the URL that identifies the requested resource, headers containing contextual data (like authentication or content type), and optionally, a body that holds additional data needed to process the request, such as forms or JSON. The server processes the request and returns a response indicating the result of the operation.

Requests are received through a DTO (Data Transfer Object). It is a way to encapsulate data in a structured and typed format to ensure that information is transmitted consistently and securely.

## Usage

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

1. Here the `CreateUserRequestDto` object is received.
```python
    async def create(self, user: CreateUserRequestDto)
```

For this example, you only need to map the fields of the `CreateUserRequestDto` class, including the `ExtraDataRequestDto` class in a JSON like this:

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

## File Upload

It is possible to create an action to upload files. For this, the request must be of type `UploadFile`.

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

The API can be consumed like this:

```sh
curl -X POST http://127.0.0.1:8000/upload \
     -F "file=@path/to/your/file"
```
