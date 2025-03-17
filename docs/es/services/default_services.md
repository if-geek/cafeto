# Servicios por defecto

## Introducción

Cafeto cuenta con algunos servicios ya diseñados para ser usados mediante inyección de dependencias.

Para usar estos servicios es necesario invocarlos.

```python
from cafeto import App

app: App = App()
app.use_default_services()
```