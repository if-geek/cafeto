# AContextService

## Introducción

Es un servicio de tipo `scoped` que puede ser inyectado para obtener información del contexto de la solicitud actual. La información que contiene este servicio es:

- `path: str`: Ruta a la cual se llegó a la acción.
- `method: str`: Método actual (`POST`, `GET`, `PUT`, `PATCH`, `DELETE`).
- `headers: Dict[str, Any]`: Las cabeceras de la solicitud.
- `query: Dict[str, Any]`: Los parámetros del query string.
- `controller_name: str`: Nombre del controlador al cual llegó la solicitud.
- `action_name: str`: Nombre de la acción a la cual llegó la solicitud.
- `request_model: BaseModel`: El DTO con el cuerpo de la solicitud, solo aplica a los métodos (`POST`, `PUT`, `PATCH`).

Para usarlo, solo se debe inyectar como cualquier otro servicio.

```python
from cafeto.services import AContextService

class MyService:
    def __init__(self, context_service: AContextService) -> None:
        self.context_service = context_service
```
