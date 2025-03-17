# Coming Soon

## Introduction

Although the system is already very effective and offers a solid set of features, continuous work is being done to improve it. The goal is to keep implementing new enhancements and functionalities to optimize the user experience. Here are some of the exciting updates to expect:

## Dependency Injection from the Controller Constructor

Allow actions that share dependencies not to need to define them in each action of the same controller.

Example:

```python
@app.controller()
class UserController(BaseController):
    def __init__(self, my_dependency: MyDependency):
        self.my_dependency = my_dependency

    @app.get('/get')
    async def get(self) -> UserResponseDto:
        await self.my_dependency.do_something()

    @app.get('/get-all')
    async def get_all(self) -> UserResponseDto:
        await self.my_dependency.do_something()
```

## Improvements to Event Functionality

Enhance the event system to make it more versatile and robust by incorporating features such as:

- Allowing events to generate responses, enabling more dynamic interactions.

- Implementing the ability for events to raise exceptions, with support for capturing and intercepting them as needed.

- Ensuring efficient error handling and controlled execution flow within events.

## Addition of New Events

Expand the current system by introducing new events. Some initial ideas include:

- **OnModeValidationFail**: An event triggered when mode validation fails, allowing for specific and customized handling of this scenario.

## Enhanced Validation System

We will implement a more advanced system for data validation.

The general idea is to create a validation system that can be used outside of DTOs and offer an easy way to return errors if they exist.

### Objectives

- **Flexibility**: Allow the use of validations in different contexts beyond DTOs.
- **Ease of Use**: Provide a simple interface for defining and managing validation rules.
- **Efficiency**: Ensure that validations are performed quickly and effectively.

## CLI Implementation

We will develop a command-line interface (CLI) for project creation.

### Examples

1. **Create a new project**:
```bash
cafeto new project-name
```

2. **Generate a controller**:
```bash
cafeto create controller user
```

### Objectives

- **Ease of Use**: Provide simple and intuitive commands for project creation and management.
- **Efficiency**: Reduce the time and effort required to initialize and configure projects.
- **Flexibility**: Allow the CLI to be extended and customized according to user needs.

## Development Templates

We will equip the system with the ability to start projects with predefined templates, avoiding starting from scratch for each new project.

## Default User and Permissions System

We will develop a system where user and permissions management is pre-designed, saving time in each new project.

## Documentation Improvements

We are working on improving the documentation, adding more examples, and providing more details about the system's features.

## Increase Parameter Support

Add the ability to support more complex data types such as lists, dates, etc.

```python
from datetime import date
from typing import List

from cafeto.mvc import BaseController


@app.controller()
class UserController(BaseController):
    @app.get('/view-filter/{ids}', query=['date'])
    async def view_filter(self, ids: List[int], date: date) -> None:
        pass
```

## Improve OpenApi Integration

We will provide more support for OpenApi features to enhance integration.

## Integration with Prometheus and Grafana

Using the template system and Docker, the ability to create logs of API events to generate system metrics will be implemented. This integration will allow developers and system administrators to monitor the performance and health of their applications more effectively.

### Objectives

- **Real-time Monitoring**: Allow real-time observation of system metrics, such as CPU usage, memory, request latency, error rates, among others.
- **Proactive Alerts**: Configure alerts to notify administrators when certain critical thresholds are reached, allowing for a quick response to potential issues.
- **Historical Analysis**: Store historical data to analyze trends and usage patterns over time, aiding in informed decision-making about infrastructure and application performance.
- **Data Visualization**: Use Grafana to create custom dashboards that clearly and comprehensively visualize the collected metrics.

## Custom Response Styles

Allow choosing between different response styles for services, not limited to JSON. The idea is to switch between `JSON`, `XML`, and `YML`.

=== "Unified style"
    ```python
    from cafeto.responses import Ok

    @app.controller()
    class UserController(BaseController):
        @app.get('/view/{id}')
        async def view(self, id: int) -> UserResponseDto:
            user = <some_user_service>.get(id)
            return Ok(UserResponseDto(**user), style='XML')
    ```

=== "Classic style"
    ```python
    from cafeto.responses import ModelResponse

    @app.controller()
    class UserController(BaseController):
        @app.get('/view/{id}')
        async def view(self, id: int) -> UserResponseDto:
            user = <some_user_service>.get(id)
            return ModelResponse(UserResponseDto(**user), style='XML')
    ```

!!! info
    **styles**

    - style='JSON' (default)
    - style='XML'
    - style='YML'


## Performance Improvements

We will optimize the system to ensure faster and more efficient performance.

## Creating an API Prefix

The functionality to add a prefix to the URLs of all API endpoints is proposed to maintain a more organized and consistent structure.

For example, using the following command:

```python
app.map_controllers(prefix='my-api')
```

This will ensure that all service routes begin with the specified prefix. The resulting URLs would look like this:

```bash
http://127.0.0.1:8000/my-api/my-controller/my-action
```

This approach simplifies the grouping of endpoints under a shared context and improves the readability and management of API routes.

## API Versioning System

Implement a versioning system for APIs that will allow developers to manage and maintain multiple versions of their APIs efficiently.

### Objectives

- **Compatibility**: Ensure that previous versions of the APIs continue to function while new versions are being developed.
- **Ease of Use**: Provide clear tools and documentation for version management.
- **Flexibility**: Allow developers to choose which versions of the APIs they want to maintain and which to deprecate.

### Example

```python
# --- main.py ---
app.map_controllers(version='v2')

# --- user_v1.py ---
@app.controller(version='v1')
class UserController(BaseController):
    @app.get('/user')
    async def get_user(self) -> UserResponseDto:
        pass

# --- user_v2.py ---
@app.controller(version='v2') #(1)
class UserController(BaseController):
    @app.get('/user')
    async def get_user(self) -> UserResponseDto:
        pass
```

1. !!! info
       **Other way**
       
       ```python
       @app.controller() # 'v2' by default
       ```

## Adaptability and Continuous Evolution

We are committed to continuous improvement and adaptation to technological advancements. The project is constantly evolving, observing trends and advancements in the software development field to implement best practices and the latest technologies.

The goal is to ensure that the system remains up-to-date and relevant, incorporating new features and optimizations that benefit users. Suggestions are welcome, and we are always open to feedback to keep improving.

### Example

- **Integration of New Technologies**: Adopt new tools and frameworks that emerge in the market.
- **Regular Updates**: Implement continuous improvements and security patches.
- **User Feedback**: Actively listen to user needs and suggestions to adapt to their requirements.