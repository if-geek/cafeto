# Access Control

## Introduction

Access control to an API is crucial to ensure that only authorized users can interact with the system's resources and data. Cafeto uses the same type of decorator as [Starlette](https://www.starlette.io/authentication/#permissions). This allows specifying which users have permission to execute certain functions, protecting the API from unauthorized access and ensuring the security and privacy of the information.

## Usage

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

`@app.requires` works in the same way as `@requires` in Starlette.
