# Controladores y acciones

## Introducción

Los controladores en una aplicación web son responsables de manejar las solicitudes del usuario, procesar datos y devolver respuestas adecuadas. Son los intermediarios entre el modelo y la vista.

Las acciones son métodos dentro de un controlador que manejan solicitudes específicas, como mostrar una página, guardar datos o realizar operaciones particulares.

En resumen, los controladores organizan la lógica de la aplicación y las acciones ejecutan tareas específicas en respuesta a las solicitudes del usuario.

## Uso

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
       Servicio simulado para el ejemplo.

Este API se puede consumir como:

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

Esto es lo mínimo requerido para la creación de un API. Los datos llegarán a la acción `create` del controlador `UserController` por el método `POST` y se almacenarán en el objeto `data`, que es del tipo `CreateUserRequestDto`. Finalmente, la respuesta será un objeto tipo `CreateUserResponseDto`.

`ModelResponse` será el encargado de devolver los datos de todos aquellos objetos (DTO) que hereden de `BaseModel`.

> **NOTA**: Es importante tipar el dato de entrada para que la asignación de los datos sea correcta.

> **NOTA**: Para indicar a Cafeto que la aplicación debe usar las acciones de los controladores, se debe usar: `app.map_controllers()`.

De igual manera, se puede usar un objeto `JSONResponse` tradicional de Starlette para la respuesta.

```python
return JSONResponse({"username": "jondoe", ...})
```

Para tener un mejor control, se recomienda usar los DTO siempre que se pueda. También es útil para ver la documentación y probar los APIs desde Swagger.

Los métodos disponibles son:

- @app.post (POST)
- @app.put (PUT)
- @app.patch (PATCH)
- @app.get (GET)
- @app.delete (DELETE)
- @app.options (OPTIONS)

> **Nota**: Solo los métodos `POST` y `PUT` pueden recibir datos como parámetro de entrada, aunque no es obligatorio.

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
       Servicio simulado para el ejemplo.

> **Nota**: Si el decorador `@app.controller` no tiene un parámetro, se usará el nombre de la clase sin la palabra "Controller".

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
       Servicio simulado para el ejemplo.

En este caso, la URL será: http://127.0.0.1:8000/user/activate
