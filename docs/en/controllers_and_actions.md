# Controllers and Actions

## Introduction

Controllers in a web application are responsible for handling user requests, processing data, and returning appropriate responses. They act as intermediaries between the model and the view.

Actions are methods within a controller that handle specific requests, such as displaying a page, saving data, or performing particular operations.

In summary, controllers organize the application's logic, and actions execute specific tasks in response to user requests.

## Usage

```python
from cafeto import App
from cafeto.mvc import BaseController
from cafeto.responses import Ok


app: App = App()

@app.controller('/user')
class UserController(BaseController):
    @app.post('/create')
    async def create(self, data: CreateUserRequestDto) -> CreateUserResponseDto:
        user = <some_user_service>.create(data) #(1)
        return Ok(CreateUserResponseDto(**user))

app.map_controllers()
```

1. !!! warning
       Simulated service for the example.

This API can be consumed as follows:

```bash
curl -X POST http://127.0.0.1:8000/user/create \
     -H "Content-Type: application/json" \
     -d '{
           "username": "superbad",
           "password": "01-47-87441",
           "confirm_password": "01-47-87441",
           "name": "McLovin",
           "birth_date": "1998-06-18"
         }'
```

This is the minimum required to create a API. The data will reach the `create` action of the `UserController` via the `POST` method and will be stored in the `data` object, which is of type `CreateUserRequestDto`. Finally, the response will be an object of type `CreateUserResponseDto`.

`ModelResponse` will be responsible for returning the data of all those objects (DTO) that inherit from `BaseModel`.

> **NOTE**: It is important to type the input data correctly to ensure proper data assignment.

> **NOTE**: To indicate to Cafeto that the application should use the controller actions, you must use: `app.map_controllers()`.

Similarly, a traditional `JSONResponse` object from Starlette can be used for the response.

```python
return JSONResponse({"username": "jondoe", ...})
```

For better control, it is recommended to use DTOs whenever possible. It is also useful for viewing documentation and testing APIs from Swagger.

The available methods are:

- @app.post (POST)
- @app.put (PUT)
- @app.patch (PATCH)
- @app.get (GET)
- @app.delete (DELETE)
- @app.options (OPTIONS)

> **Note**: Only `POST` and `PUT` methods can receive data as input parameters, although it is not mandatory.

```python
from cafeto.mvc import BaseController
from cafeto.responses import Ok


@app.controller('/user')
class UserController(BaseController):
    @app.post('/activate')
    async def activate(self) -> CreateUserResponseDto:
        user = <some_user_service>.get() #(1)
        return Ok(CreateUserResponseDto(**user))
```

1. !!! warning
       Simulated service for the example.

> **Note**: If the `@app.controller` decorator does not have a parameter, the class name will be used without the word "Controller".

```python
from cafeto.mvc import BaseController
from cafeto.responses import Ok


@app.controller() # No param
class UserController(BaseController):
    @app.post('/activate')
    async def activate(self) -> CreateUserResponseDto:
        user = <some_user_service>.get() #(1)
        return Ok(CreateUserResponseDto(**user))
```

1. !!! warning
       Simulated service for the example.

In this case, the URL will be: http://127.0.0.1:8000/user/activate