# DTO

## Introduction

A DTO (Data Transfer Object) is a design pattern used in software development to facilitate the transfer of data between different layers or components of an application. Its functionality focuses on three key aspects:

1. Obtaining data from the request: DTOs are responsible for receiving the data provided by the client in requests, encapsulating them in a structured and clear manner.

2. Data validation and quality: Before the data is processed or stored, the DTO ensures that it meets validation requirements, such as correct data types, expected values, and possible constraints. This ensures the integrity and quality of the information within the application.

3. Bridge between client and internal data: They act as intermediaries between client requests and the internal layers of the system, such as the business logic layer or the persistence layer. This decouples the internal structures of the system from external interactions, promoting a more flexible and maintainable design.

In summary, a DTO not only organizes incoming data but also ensures that it is consistent and serves the role of efficiently connecting the client with internal processes.

Cafeto uses [Pydantic](https://docs.pydantic.dev/latest/) as the library for creating DTOs.

## Usage

```python
from datetime import date

from cafeto.models import BaseModel


class CreateUserRequestDto(BaseModel):
    username: str
    password: str
    confirm_password: str
    name: str
    birth_date: date


class CreateUserResponseDto(BaseModel):
    id: int
    username: str
    name: str
    birth_date: date
```

Here, two DTOs are defined, one for data input (Request) and one for data output (Response).

> **Note**: The `BaseModel` class comes from `cafeto.models`, which inherits from `BaseModel` of [Pydantic](https://docs.pydantic.dev/latest/), as some necessary functions have been added.

A good strategy is to use a base class to share fields related to the `request` and `response`. This way, the classes that inherit from it can reuse these fields, avoiding the need to define them multiple times.

```python
from datetime import date

from cafeto.models import BaseModel


class BaseUserDto(BaseModel):
    username: str
    name: str
    birth_date: date


class CreateUserRequestDto(BaseUserDto):
    password: str
    confirm_password: str


class CreateUserResponseDto(BaseUserDto):
    id: int
```

It is possible to achieve a robust enough configuration to organize DTOs more efficiently, ensuring clarity and order in their structure.

```python
from datetime import date

from cafeto.models import BaseModel


class BaseUserDto(BaseModel):
    username: str
    name: str
    birth_date: date


class BaseUserRequestDto(BaseUserDto):
    password: str
    confirm_password: str


class BaseUserResponseDto(BaseUserDto):
    id: int


class CreateUserRequestDto(BaseUserRequestDto):
    ...


class UpdateUserRequestDto(BaseUserRequestDto):
    old_password: str


class CreateUserResponseDto(BaseUserResponseDto):
    ...


class UpdateUserResponseDto(BaseUserResponseDto):
    ...
```