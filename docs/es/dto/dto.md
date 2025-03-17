# DTO

## Introducción

Un DTO (Data Transfer Object) es un patrón de diseño utilizado en el desarrollo de software para facilitar la transferencia de datos entre diferentes capas o componentes de una aplicación. Su funcionamiento se centra en tres aspectos clave:

1. Obtención de datos desde el request: Los DTOs se encargan de recibir los datos proporcionados por el cliente en solicitudes (requests), encapsulándolos de manera estructurada y clara.

2. Validación y calidad de los datos: Antes de que los datos se procesen o se almacenen, el DTO garantiza que cumplan con los requisitos de validación, como tipos de datos correctos, valores esperados, y posibles restricciones. Esto asegura la integridad y calidad de la información dentro de la aplicación.

3. Puente entre cliente y datos internos: Actúan como intermediarios entre las solicitudes del cliente y las capas internas del sistema, como la capa de lógica de negocio o la de persistencia. Esto desacopla las estructuras internas del sistema de las interacciones externas, promoviendo un diseño más flexible y mantenible.

En resumen, un DTO no solo organiza los datos entrantes, sino que también asegura que sean consistentes y cumple con el rol de conectar de manera eficiente al cliente con los procesos internos.

Cafeto usa [Pydantic](https://docs.pydantic.dev/latest/) como librería para la creación de los DTO.

## Uso

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

Aquí se definen dos DTO, uno para la entrada de datos (Request) y otro para la salida (Response).

> **Nota**: La clase `BaseModel` viene de `cafeto.models`, que hereda de `BaseModel` de [Pydantic](https://docs.pydantic.dev/latest/), ya que se han añadido algunas funciones necesarias.


Una buena estrategia es utilizar una clase base para compartir los campos relacionados con el `request` y el `response`. De esta manera, las clases que hereden de ella podrán reutilizar estos campos, evitando la necesidad de definirlos varias veces.


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


Es posible lograr una configuración lo suficientemente robusta como para organizar de manera más eficiente los DTOs, garantizando claridad y orden en su estructura.


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
