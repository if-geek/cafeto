# AContextService

## Introduction

It is a `scoped` type service that can be injected to obtain information about the current request context. The information contained in this service includes:

- `path: str`: The path to which the action was reached.
- `method: str`: The current method (`POST`, `GET`, `PUT`, `PATCH`, `DELETE`).
- `headers: Dict[str, Any]`: The request headers.
- `query: Dict[str, Any]`: The query string parameters.
- `controller_name: str`: The name of the controller to which the request was directed.
- `action_name: str`: The name of the action to which the request was directed.
- `request_model: BaseModel`: The DTO with the request body, only applicable to (`POST`, `PUT`, `PATCH`) methods.

To use it, simply inject it like any other service.

```python
from cafeto.services import AContextService

class MyService:
    def __init__(self, context_service: AContextService) -> None:
        self.context_service = context_service
```