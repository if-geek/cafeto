# Cafeto

Cafeto es un framework liviano pero poderoso diseñado como una capa superior sobre [Starlette](https://www.starlette.io/), enfocado en simplificar y acelerar el desarrollo de APIs modernas. Aprovecha las sólidas bases de [Starlette](https://www.starlette.io/), ofreciendo herramientas adicionales para un desarrollo más eficiente y organizado.

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
from typing import Dict

from cafeto import App
from cafeto.mvc import BaseController
from cafeto.responses import Ok


app: App = App()

@app.controller('/home')
class HomeController(BaseController):
    @app.get('/hello')
    async def hello(self, name: str) -> Dict[str, str]:
        return Ok({'Hello': 'World!'})

app.map_controllers()

```

Para más detalles de uso, mira las [caracteristicas](https://if-geek.github.io/cafeto/)


## Licencia

Este proyecto está licenciado bajo la [Licencia MIT](LICENSE)

## Contacto

Jonathan Espinal - jonathan.espinal@gmail.com

## Documentación

[Caracteristicas](docs/FEATURES.es.md)

[Próximos pasos](docs/NEXT_STEPS.es.md)
