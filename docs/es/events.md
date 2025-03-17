# Eventos

## Introducción

Cafeto presenta tres tipos de eventos que se pueden usar para realizar acciones globales sobre las solicitudes. Estas acciones se aplicarán a cada acción en toda la aplicación y se ejecutarán en el orden en que se agreguen.

Los eventos son similares a los Middleware, pero son más sencillos de implementar y proporcionan acceso a una gran cantidad de información del sistema sobre la solicitud en curso.

Los eventos disponibles en Cafeto son: `OnBeforeAction`, `OnExecuteAction` y `OnAfterAction`.

## OnBeforeAction

Se ejecuta antes de la ejecución de la acción del controlador y recibe dos parámetros: `controller: BaseController` y `action: Action`.

```python
from cafeto import App
from cafeto.mvc import BaseController
from cafeto.events import OnBeforeAction
from cafeto.types import Action

app: App = App()

def get_on_before_action(controller: BaseController, action: Action):
    # Your Code

OnBeforeAction.add(get_on_before_action)
```

## OnExecuteAction

Se ejecuta junto con la ejecución de la acción del controlador y recibe tres parámetros: `controller: BaseController`, `action: Action` y `request_model: BaseModel`.

```python
from cafeto import App
from cafeto.mvc import BaseController
from cafeto.events import OnExecuteAction
from cafeto.types import Action

app: App = App()

def get_on_execute_action(controller: BaseController, action: Action, request_model: BaseRequest):
    # Your Code

OnExecuteAction.add(get_on_execute_action)
```

## OnAfterAction

Se ejecuta después de la ejecución de la acción del controlador y recibe cuatro parámetros: `controller: BaseController`, `action: Action`, `request_model: BaseModel` y `response: Response`.

```python
from cafeto import App
from cafeto.mvc import BaseController
from cafeto.events import OnAfterAction
from cafeto.types import Action
from cafeto.responses import Response

app: App = App()

def get_on_after_action(controller: BaseController, action: Action, request_model: BaseRequest, response: Response):
    # Your Code

OnAfterAction.add(get_on_after_action)
```

Los eventos también pueden ser removidos.

```python
OnAfterAction.remove(get_on_after_action)
```

Los eventos también pueden ser asíncronos.

```python
from cafeto import App
from cafeto.mvc import BaseController
from cafeto.events import OnAfterAction
from cafeto.types import Action
from cafeto.responses import Response

app: App = App()

async def get_on_after_action(controller: BaseController, action: Action, request_model: BaseRequest, response: Response):
    # Your Code

OnAfterAction.add(get_on_after_action)
```
