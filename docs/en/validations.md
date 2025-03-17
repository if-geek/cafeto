# Validations

## Introduction

Validations in an API are processes that verify that the data sent to the server meets certain rules or criteria before being processed. This ensures that the information is correct, complete, and secure.

## Importance

- **Error Prevention**: Prevents incorrect data from causing system failures.
- **Security**: Protects against code injections and other attacks.
- **Data Integrity**: Ensures that stored and processed data is consistent and reliable.
- **User Experience**: Provides immediate feedback on errors in the submitted data.

Essential for robust and secure API operation!

## Usage

In Cafeto, DTOs will execute the validations that Pydantic has available by default.

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

In the example above, the fields `username`, `password`, `confirm_password`, and `birth_date` are required, while the `name` field is optional, and the `username` field has a minimum length of 3 characters. These validations will be executed automatically when the action is consumed, and errors will be returned with a `statusCode` of `400`.

For custom validations, there is the `@validate` decorator. This decorator takes the name of the field to be validated as a parameter; if this field is not provided, the entire DTO will be validated.

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

1. Validates the `password` field.

2. Validates the `birth_date` field.

3. Validates the entire model.

The `@validate` decorator is similar to Pydantic's `@field_validator` and was developed to create custom and asynchronous validations. It also supports dependency injection in the method to which it is applied.

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

If we send the above request, we will get the following result:

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

This is more or less the same format in which Pydantic returns data validation.

`FieldError` is used to throw an exception when a DTO field fails and takes an `Error` object as a parameter, which in turn takes the parameters `type: str` and `msg: str`. There is a third parameter called `loc: List[str | int] | str | int`; if this is not used, Pydantic will do it automatically.

In the `loc` array, the word `__model__` refers to global errors, i.e., those not necessarily associated with any DTO field.

## Important Information

It is important to note that these methods are static, so they do not receive the `self` parameter.

The parameters of the method where the `@validate` decorator is applied are: `value` and `data`.

1. **value**: It is the current value of the field being validated, and the data type will be the one configured from the model.
> **Note**: If the validator applies to the entire model, the first parameter will be a dictionary with the data of the entire model.

2. **data**: It is a dictionary with the other fields of the model.
> **Note**: If the validator applies to the entire model, the second parameter does not exist.

As a general rule, if the second parameter is not needed, it is usually called "_" (underscore).

```python
@validate('birth_date') #(2)
def validate_birth_date(value: date, _: Dict[str, Any]) -> date:
```

## Error Format

There is an additional way to return errors; for this, the application must be configured to return them in this format.

```python
from cafeto import CafetoConfig

config: CafetoConfig = CafetoConfig(error_object=True)
app: App = App(config=config)
```

In that case, errors will be thrown in both the previously seen format and the new one.

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

In this case, two types of errors are thrown: `errorList` and `errorObject`. In the latter, the `loc` field no longer exists and becomes the nested keys of the object with the errors.

## Modifying Values

The `@validate` decorator also serves to modify the DTO values when returned, i.e., it can be used not only to validate data but also to alter their values.

> **Note**: It is important to note that validators **always** must return a value; this value will be the one finally used in the model.

```python
class MyModelDto(BaseModel):
    name: str

    @validate('name')
    def validate_name(value: str, _: Dict[str, Any]) -> str:
        return value + ' - Hello'
```

The value of the `name` field will be the assigned value + " - Hello".

## Nested Models

If you need to validate a model where one of its fields is another model, you must pay attention to how these are validated. If we use the `@validate` decorator on the field that contains the nested model, the custom validations of this model will not be executed. This is because the system must determine which validation to execute and will prioritize the one that is less nested in the model.

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

In this last example, the `validate_name_a` validation and any other in the `MyModelA` model will not be executed because the `validate_model_a_from_b` validation in the `MyModelB` model is overwriting it.

## Validators

As seen in the previous examples, validations are associated with DTOs. However, it may not always be desirable to have this behavior. For these cases, there are validators. These are classes to which the `@validate` decorator is also applied, either to validate a field or the entire model, just like DTOs. To use these validators, you only need to inherit from the `BaseValidator` class.

```python
from cafeto.models import BaseValidator, validate

class MyValidator(BaseValidator):
    @validate('name')
    def validate_name(value: str, _: Dict[str, Any]) -> str:
        if value == '??':
            raise FieldError(Error('name-error', 'Name Error'))
        return value
```

Dependencies can also be injected into validators, just like DTOs.

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

To use the validator, it must be configured in the controller action. This is done in the `body` parameter of the `@app.get`, `@app.post`, `@app.put`, `@app.patch`, and `@app.delete` decorators.

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

In this example, the DTO's own validations, such as the required fields (`name`, `age`), will be applied. Additionally, custom validations will be executed using the `MyValidator` validator. This is particularly useful if you want to keep a cleaner DTO and reuse these validations across different DTOs.

It is possible to have nested validators, just like DTOs.

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

It doesn't matter if the field to be validated is a list or a dictionary; the configuration remains the same.

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

There is also the possibility of not validating the DTO at all and delegating this task to a manual process. To do this, `None` should be sent in the `body` property instead of the validator.

```python
@app.controller()
class MyController(BaseController):
    @app.post('/create', body={'validator': None})
    async def create(self, request: MyDto):
        # Code
```

In this case, the `request` parameter will contain the values sent via the `POST` method, but without validations.

The DTO can be validated later using the following code:

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

If you want to use a different validator than the DTO, it should be passed as a parameter to the `check` method.

```python
try:
    await request.check(MyValidator)
except ModelError e:
    print(e.errors)
```

It is possible to return these errors as they are generated by the exception when validating the model, or format them to match the format normally used when validations are performed automatically.

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
