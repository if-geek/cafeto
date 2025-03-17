# Events

## Introduction

Cafeto provides three types of events that can be used to perform global actions on requests. These actions will be applied to each action throughout the application and will be executed in the order they are added.

Events are similar to Middleware but are simpler to implement and provide access to a wealth of system information about the current request.

The events available in Cafeto are: `OnBeforeAction`, `OnExecuteAction`, and `OnAfterAction`.

## OnBeforeAction

This event is executed before the controller action is executed and receives two parameters: `controller: BaseController` and `action: Action`.

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

This event is executed along with the controller action and receives three parameters: `controller: BaseController`, `action: Action`, and `request_model: BaseModel`.

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

This event is executed after the controller action is executed and receives four parameters: `controller: BaseController`, `action: Action`, `request_model: BaseModel`, and `response: Response`.

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

Events can also be removed.

```python
OnAfterAction.remove(get_on_after_action)
```

Events can also be asynchronous.

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