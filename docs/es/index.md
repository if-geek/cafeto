# Cafeto

## Introducción

Cafeto es un framework liviano pero poderoso diseñado como una capa superior sobre [Starlette](https://www.starlette.io/), enfocado en simplificar y acelerar el desarrollo de APIs modernas. Aprovecha las sólidas bases de [Starlette](https://www.starlette.io/), ofreciendo herramientas adicionales para un desarrollo más eficiente y organizado.

[:flag_us: English](/cafeto) | [:flag_co: Español](/cafeto/es)

## Requisitos

Este proyecto requiere **Python 3.10** o una versión superior.

## Instalación

```bash
pip install cafeto
```

## Proyecto

[Cafeto](https://github.com/if-geek/cafeto/)

## Documentacián

[Cafeto docs](https://if-geek.github.io/cafeto/)

## Descripción

Cafeto es un framework diseñado para crear APIs de manera eficiente y organizada, inspirado en otros frameworks y enriquecido con ideas innovadoras.

- Ofrece un poderoso sistema de inyección de dependencias, soportando los tres ciclos de vida: `Singleton`, `Scoped` y `Transient`.
- Facilita la recepción y envío de información mediante DTOs (Data Transfer Objects), que también se utilizan para la validación y gestión de los datos que interactúan con el servidor.
- Cuenta con un sistema de eventos que amplía las capacidades del framework, permitiendo una mayor personalización y flexibilidad.
- Proporciona integración con herramientas como OpenAPI y Swagger, para la generación de documentación interactiva y pruebas de las APIs.

Con Cafeto, los desarrolladores pueden construir APIs robustas y escalables con facilidad, aprovechando características modernas y un enfoque bien estructurado.

## Starlette

Starlette, la base de Cafeto, es ampliamente reconocido como uno de los frameworks más destacados para la construcción de aplicaciones web asincrónicas en Python. Su diseño minimalista, combinado con un rendimiento sobresaliente, lo hace ideal para desarrolladores que buscan flexibilidad y potencia. Starlette no solo ofrece capacidades de routing, middleware y soporte para WebSockets, sino que también integra herramientas avanzadas para manejo de tareas asíncronas y pruebas, posicionándose como un estándar dorado en el desarrollo web moderno.

Aprovechando el poder de Starlette, Cafeto lleva esta experiencia al siguiente nivel, proporcionando una solución aún más optimizada y amigable para construir APIs. Juntos, Cafeto y Starlette forman un dúo perfecto para cualquier desarrollador que busque velocidad, simplicidad y excelencia técnica.

## Objetivo Principal

Crear una experiencia de desarrollo más fluida para APIs, proporcionando abstracciones intuitivas, configuraciones predeterminadas inteligentes y compatibilidad con estándares modernos.

## Ejemplo

```python
import uvicorn

from cafeto import App
from cafeto.mvc import BaseController
from cafeto.responses import Ok
from cafeto.models import BaseModel


app: App = App()

class CreateUserRequestDto(BaseModel):
    username: str
    password: str


class CreateUserResponseDto(BaseModel):
    id: int
    username: str


@app.controller('/user')
class UserController(BaseController):
    @app.post('/create')
    async def create(self, data: CreateUserRequestDto) -> CreateUserResponseDto:
        user = {'id': 1, 'username': data.username}
        return Ok(CreateUserResponseDto(**user))

app.map_controllers()

if __name__ == "__main__": #(1)
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
```

1. También se puede ejecutar por comando:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Este ejemplo muestra cómo definir un controlador y dos DTOs (uno para la solicitud y otro para la respuesta), y cómo configurar una ruta para crear un usuario.

La clase `App` hereda de la clase `Starlette`, lo que implica que las propiedades de Starlette también están disponibles en la clase App. Un ejemplo de estas propiedades son los `Middleware`. Sin embargo, existe una configuración adicional llamada `CafetoConfig`, la cual se explicará más adelante.

```python
from cafeto.middleware import CORSMiddleware

middleware = [
    Middleware(CORSMiddleware, allow_origins=['*'])
]

app: App = App(debug=True, middleware=middleware)
```

## Conclusión

Cafeto es una herramienta poderosa que facilita la creación de APIs en Python. Con soporte para inyección de dependencias, DTOs y documentación automática, es una excelente opción para desarrolladores que buscan una solución simple pero profesional para sus proyectos de API.
