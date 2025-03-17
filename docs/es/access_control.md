# Control de Acceso

## Introducción

El control de acceso a un API es crucial para asegurar que solo usuarios autorizados puedan interactuar con los recursos y datos del sistema. Cafeto usa el mismo tipo de decorador de [Starlette](https://www.starlette.io/authentication/#permissions). De esta forma se permite especificar qué usuarios tienen permiso para ejecutar ciertas funciones, protegiendo la API de accesos no autorizados y garantizando la seguridad y privacidad de la información.

## Uso

```python
from cafeto import App
from cafeto.mvc import BaseController
from cafeto.responses import Ok


app: App = App()

@app.controller()
class UserController(BaseController):
    @app.get('/view')
    @app.requires(['admin'])
    async def view(self) -> str:
        return Ok('Hello World!')
```

`@app.requires` funciona de la misma manera que `@requires` de Starlette.
