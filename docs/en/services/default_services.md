# Default Services

## Introduction

Cafeto includes some pre-designed services that can be used through dependency injection.

To use these services, you need to invoke them.

```python
from cafeto import App

app: App = App()
app.use_default_services()
```