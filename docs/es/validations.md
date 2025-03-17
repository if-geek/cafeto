# Validaciones

## Introducción

Las validaciones en una API son procesos que verifican que los datos enviados al servidor cumplen con ciertas reglas o criterios antes de ser procesados. Esto asegura que la información sea correcta, completa y segura.

## Importancia

- **Prevención de errores**: Evita que datos incorrectos causen fallos en el sistema.
- **Seguridad**: Protege contra inyecciones de código y otros ataques.
- **Integridad de datos**: Garantiza que los datos almacenados y procesados sean consistentes y confiables.
- **Experiencia del usuario**: Proporciona retroalimentación inmediata sobre errores en los datos enviados.

¡Esencial para un funcionamiento robusto y seguro de la API!

## Uso

En Cafeto, los DTO ejecutarán las validaciones que Pydantic tiene disponibles por defecto.

```python
from typing import Optional
from pydantic import Field
from cafeto import BaseModel


class CreateUserRequestDto(BaseModel):
    username: str = Field(min_length=3)
    password: str
    confirm_password: str
    name: Optional[str]
    birth_date: date
```

En el ejemplo anterior, los campos `username`, `password`, `confirm_password` y `birth_date` son obligatorios, mientras que el campo `name` es opcional, y el campo `username` tiene un límite mínimo de 3 caracteres. Estas validaciones se ejecutarán automáticamente cuando se consuma la acción y los errores se retornarán con un `statusCode` `400`.

Para las validaciones personalizadas, existe el decorador `@validate`. Este decorador recibe como parámetro el nombre del campo a validar; si no se provee este campo, se validará todo el modelo.

```python
from datetime import date
from typing import Any, Optional, Dict, List

from pydantic import Field
from cafeto import App
from cafeto.models import BaseModel, validate
from cafeto.errors import FieldError, ModelError, Error
from cafeto.mvc import BaseController
from cafeto.responses import Ok


class ExtraDataRequestDto(BaseModel):
    nickname: str


class CreateUserRequestDto(BaseModel):
    username: str
    password: str = Field(min_length=3)
    confirm_password: str
    name: Optional[str]
    birth_date: date
    extra_data: ExtraDataRequestDto

    @validate('password') #(1)
    def validate_password(value: str, data: Dict[str, Any]) -> str:
        if value != data.get('confirm_password', None):
            raise FieldError(Error('same-password', 'Password and confirm password must be the same'))
        return value

    @validate('birth_date') #(2)
    def validate_birth_date(value: date, data: Dict[str, Any]) -> date:
        if value.year <= 2000:
            raise FieldError(Error('year-error', 'The year must be greater than 2000'))
        return value

    @validate() #(3)
    async def validate(data: Dict[str, Any]) -> Dict[str, Any]:
        errors: List[Error] = []
        errors.append(Error('user-custom', 'Custom error'))
        if len(errors) > 0:
            raise ModelError(errors)

        return data

app: App = App()

@app.controller('/user')
class UserController(BaseController):
    @app.post('/create')
    async def create(self, user: CreateUserRequestDto) -> Dict[str, str]:
        return Ok({'hello': 'HomepageController'})

app.map_controllers()
```

1. Valida el campo `password`.

2. Valida el campo `birth_date`.

3. Valida todo el modelo.

El decorador `@validate` es similar a `@field_validator` de Pydantic y se desarrolló con el fin de poder crear validaciones personalizadas y asíncronas. También soporta inyección de dependencias en el método sobre el cual se aplica.

```sh
curl -X PUT http://127.0.0.1/user/create \
     -H "Content-Type: application/json" \
     -d '{
           "password": "pa",
           "confirm_password": "other-password-123",
           "birth_date": "1998-06-18",
           "extra_data": {}
         }'
```

Si enviamos la solicitud anterior, obtendremos el siguiente resultado:

```json
{
    "errorList": [
        {
            "loc": [
                "__model__"
            ],
            "type": "user-custom",
            "msg": "Custom error"
        },
        {
            "loc": [
                "password"
            ],
            "type": "same-password",
            "msg": "Password and confirm password must be the same"
        },
        {
            "loc": [
                "birth_date"
            ],
            "type": "year-error",
            "msg": "The year must be greater than 2000"
        },
        {
            "loc": [
                "username"
            ],
            "type": "missing",
            "msg": "Field required"
        },
        {
            "loc": [
                "password"
            ],
            "type": "string_too_short",
            "msg": "String should have at least 3 characters"
        },
        {
            "loc": [
                "name"
            ],
            "type": "missing",
            "msg": "Field required"
        },
        {
            "loc": [
                "extra_data",
                "nickname"
            ],
            "type": "missing",
            "msg": "Field required"
        }
    ]
}
```

Este es más o menos el mismo formato en que Pydantic retorna la validación de los datos.

`FieldError` se usa para lanzar una excepción cuando falla un campo del DTO y recibe como parámetro un objeto `Error`, que a su vez recibe los parámetros `type: str` y `msg: str`. Existe un tercer parámetro llamado `loc: List[str | int] | str | int`; si este no se usa, Pydantic lo hará automáticamente.

En el arreglo `loc`, la palabra `__model__` hace referencia a errores globales, es decir, que no están necesariamente asociados a ningún campo del DTO.

## Información importante

Es importante notar que estos métodos son estáticos, por lo que no reciben el parámetro `self`.

Los parámetros del método donde se aplica el decorador `@validate` son: `value` y `data`.

1. **value**: Es el valor actual del campo que se está validando y el tipo de dato será el que se configuró desde el modelo.
> **Nota**: Si el validador aplica para todo el modelo, el primer parámetro será un diccionario con los datos de todo el modelo.

2. **data**: Es un diccionario con los demás campos del modelo.
> **Nota**: Si el validador aplica para todo el modelo, el segundo parámetro no existe.

Como regla general, si no se necesita hacer uso del segundo parámetro, se suele llamar "_" (guion bajo).

```python
@validate('birth_date') #(2)
def validate_birth_date(value: date, _: Dict[str, Any]) -> date:
```

## Formato de los errores

Existe una forma adicional de retornar errores; para ello, se debe configurar la aplicación para que los retorne con este formato.

```python
from cafeto import CafetoConfig

config: CafetoConfig = CafetoConfig(error_object=True)
app: App = App(config=config)
```

En ese caso, los errores se lanzarán con los dos formatos, el anteriormente visto y el nuevo.

```json
{
    "errorList": [
        {
            "loc": [
                "__model__"
            ],
            "type": "user-custom",
            "msg": "Custom error"
        },
        {
            "loc": [
                "password"
            ],
            "type": "same-password",
            "msg": "Password and confirm password must be the same"
        },
        {
            "loc": [
                "birth_date"
            ],
            "type": "year-error",
            "msg": "The year must be greater than 2000"
        },
        {
            "loc": [
                "username"
            ],
            "type": "missing",
            "msg": "Field required"
        },
        {
            "loc": [
                "password"
            ],
            "type": "string_too_short",
            "msg": "String should have at least 3 characters"
        },
        {
            "loc": [
                "name"
            ],
            "type": "missing",
            "msg": "Field required"
        },
        {
            "loc": [
                "extra_data",
                "nickname"
            ],
            "type": "missing",
            "msg": "Field required"
        }
    ],
    "errorObject": {
        "__model__": [
            {
                "type": "user-custom",
                "msg": "Custom error"
            }
        ],
        "password": [
            {
                "type": "same-password",
                "msg": "Password and confirm password must be the same"
            },
            {
                "type": "string_too_short",
                "msg": "String should have at least 3 characters"
            }
        ],
        "birth_date": [
            {
                "type": "year-error",
                "msg": "The year must be greater than 2000"
            }
        ],
        "username": [
            {
                "type": "missing",
                "msg": "Field required"
            }
        ],
        "name": [
            {
                "type": "missing",
                "msg": "Field required"
            }
        ],
        "extra_data": {
            "nickname": [
                {
                    "type": "missing",
                    "msg": "Field required"
                }
            ]
        }
    }
}
```

En este caso, se lanzan dos tipos de errores: `errorList` y `errorObject`. En este último, el campo `loc` deja de existir y se convierte en las llaves anidadas del objeto con los errores.

## Modificar valores

El decorador `@validate` también sirve para modificar los valores del DTO al ser devueltos, es decir, no solo se pueden usar para validar datos sino para alterar los valores de estos.

> **Nota**: Es importante anotar que los validadores **siempre** deben devolver un valor, este valor será el que finalmente se usará en el modelo.

```python
class MyModelDto(BaseModel):
    name: str

    @validate('name')
    def validate_name(value: str, _: Dict[str, Any]) -> str:
        return value + ' - Hello'
```

El valor del campo `name` será el valor asignado + " - Hello".

## Modelos anidados

Si se requiere validar un modelo, donde uno de sus campos es otro modelo, debe poner atención en la forma como estos se validan. Si usamos el decorador `@validate` sobre el campo que contiene el modelo anidado, no se realizarán las validaciones personalizadas de este. Esto se debe a que el sistema debe determinar cuál validación se debe ejecutar y se dará prioridad a aquella que esta menos inmersa en el modelo.

```python
class MyModelA(BaseModel):
    name_a: str

    @validate('name_a')
    def validate_name_a(value: str, _: Dict[str, Any]) -> str:
        return value + ' - Hello A from MyModelA'


class MyModelB(BaseModel):
    name_b: str
    model_a: MyModelA

    @validate('name_b')
    def validate_name_b(value: str, _: Dict[str, Any]) -> str:
        return value + ' - Hello B'

    @validate('model_a')
    def validate_model_a_from_b(value: MyModelA, _: Dict[str, Any]) -> MyModelA:
        value.name_a += ' - Hello A from MyModelB'
        return value
```

En este último ejemplo, la validación `validate_name_a` y ninguna otra que se encuentre en el modelo `MyModelA` se ejecutará, debido a que la validación `validate_model_a_from_b` del modelo `MyModelB` la está sobrescribiendo.

## Validadores

Como se puede observar en los ejemplos anteriores, las validaciones están asociadas a los DTO. Sin embargo, es posible que no siempre se desee este comportamiento. Para estos casos, existen los validadores. Estos son clases a los que también se les aplica el decorador `@validate`, ya sea para validar un campo o todo el modelo, al igual que los DTO. Para utilizar estos validadores, solo es necesario heredar de la clase `BaseValidator`.

```python
from cafeto.models import BaseValidator, validate

class MyValidator(BaseValidator):
    @validate('name')
    def validate_name(value: str, _: Dict[str, Any]) -> str:
        if value == '??':
            raise FieldError(Error('name-error', 'Name Error'))
        return value
```

A los validadores también se les pueden inyectar dependencias, al igual que a los DTO.

```python
from cafeto.models import BaseValidator, validate

class MyValidator(BaseValidator):
    @validate()
    async def validate_model(value: Dict[str, Any], some_service: ASomeService) -> Dict[str, Any]:
        result = await some_service.validate_user(value.get('user'))
        if not result:
            raise ModelError([Error('name-error', 'Name Error')])
        return value
```

Para hacer uso del validador, este debe configurarse en la acción del controlador. Esto se realiza en el parámetro `body` de los decoradores `@app.get`, `@app.post`, `@app.put`, `@app.patch` y `@app.delete`.

```python
from cafeto.models import BaseModel, BaseValidator, validate
from cafeto.mvc import BaseController

class MyDto(BaseModel):
    name: str
    age: int


class MyValidator(BaseValidator):
    @validate('name')
    def validate_name(value: str, _: Dict[str, Any]) -> str:
        if value == '??':
            raise FieldError(Error('name-error', 'Name Error'))
        return value


@app.controller()
class MyController(BaseController):
    @app.post('/create', body={'validator': MyValidator})
    async def create(self, request: MyDto):
        # Code
```

En este ejemplo, las validaciones propias del DTO, como los campos requeridos (`name`, `age`), serán aplicados. Además, las validaciones personalizadas se ejecutarán utilizando el validador `MyValidator`. Esto es particularmente útil si se desea mantener un DTO más limpio y reutilizar dichas validaciones entre diferentes DTO.

Es posible tener validadores anidados, al igual que los DTO.

```python
class MyDto(BaseModel):
    name: str

class MyComplexDto(BaseModel):
    complex_name: str
    my_dto: MyDto

class MyValidator(BaseValidator):
    @validate('name')
    def validate_name(value: str, _: Dict[str, Any]) -> str:
        # Validation Code

class MyComplexValidator(BaseValidator):
    my_dto: MyValidator

    @validate('complex_name')
    def validate_complex_name(value: str, _: Dict[str, Any]) -> str:
        # Validation Code
```

No importa si el campo a validar es una lista o un diccionario; la configuración permanece igual.

```python
class MyDto(BaseModel):
    name: str

class MyComplexDto(BaseModel):
    complex_name: str
    my_dto_list: List[MyDto]

class MyValidator(BaseValidator):
    @validate('name')
    def validate_name(value: str, _: Dict[str, Any]) -> str:
        # Validation Code

class MyComplexValidator(BaseValidator):
    my_dto_list: MyValidator

    @validate('complex_name')
    def validate_complex_name(value: str, _: Dict[str, Any]) -> str:
        # Validation Code
```

También existe la posibilidad de no validar el DTO en absoluto y delegar esta tarea a un proceso manual. Para ello, se debe enviar `None` en la propiedad `body` en lugar del validador.

```python
@app.controller()
class MyController(BaseController):
    @app.post('/create', body={'validator': None})
    async def create(self, request: MyDto):
        # Code
```

En este caso, el parámetro `request` contendrá los valores enviados mediante el método `POST`, pero sin validaciones.

El DTO puede ser validado posteriormente mediante el siguiente código:

```python
@app.controller()
class MyController(BaseController):
    @app.post('/create', body={'validator': None})
    async def create(self, request: MyDto):
        try:
            await request.check()
        except ModelError e:
            print(e.errors)

        # More Code
```

Si se desea usar un validador diferente al DTO, este se debe pasar como parámetro al método `check`.

```python
try:
    await request.check(MyValidator)
except ModelError e:
    print(e.errors)
```

Es posible retornar estos errores tal y como los genera la excepción al momento de hacer la validación del modelo, o formatearlos para que coincidan con el formato que normalmente se utiliza cuando las validaciones se realizan de forma automática.

```python
from cafeto.errors import format_errors
from cafeto.responses import BadRequest

@app.controller()
class MyController(BaseController):
    @app.post('/create', body={'validator': None})
    async def create(self, request: MyDto):
        try:
            await request.check()
        except ModelError e:
            errors = format_errors(e.errors)
            return BadRequest(errors)

        # More Code
```
