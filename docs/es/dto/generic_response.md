# GenericResponseDto

## Introducción

Este DTO se utiliza para enviar respuestas que contienen un valor genérico.

```python
from cafeto.dtos import GenericResponseDto

@app.controller()
class HomeController(BaseController):
    @app.get('/home')
    async def home(self) -> GenericResponseDto[str]:
        # Response Generic str
        return Ok(GenericResponseDto(data='Hello World!'))
```

```python
from cafeto.dtos import GenericResponseDto

@app.controller()
class HomeController(BaseController):
    @app.get('/home')
    async def home(self) -> GenericResponseDto[Dict[str, str]]:
        # Response Generic Dict
        return Ok(GenericResponseDto(data={'Hello': 'World!'}))
```
