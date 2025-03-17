# Schema

## Introduction

Using a schema like OpenAPI to display the inputs and outputs of an API offers several significant advantages:

- **Clear and detailed documentation**: OpenAPI allows you to create comprehensive documentation that describes the endpoints, HTTP methods, parameters, responses, and other elements of the API. This makes it easier for other developers to understand and use the API.

- **Facilitates collaboration**: With well-defined documentation, development teams can collaborate more effectively. Developers can quickly understand how to interact with the API, reducing the need for additional communication.

- **Simplifies testing and debugging**: Tools like Swagger UI provide an interactive graphical interface for testing and exploring APIs. This allows developers and testers to quickly verify the functionality of endpoints and detect potential errors.

- **Standardization**: OpenAPI follows a recognized standard for defining and describing APIs. This ensures that the documentation is consistent and understandable, regardless of who created it.

- **Automatic code generation**: Many tools can automatically generate client and server code from an OpenAPI specification. This speeds up development and ensures that the generated code is aligned with the documentation.

- **Improves maintainability**: Having up-to-date and accurate documentation makes it easier to maintain the API. Changes to endpoints, parameters, or responses can be quickly reflected in the documentation, ensuring that all API users are aware of the modifications.

- **Data validation**: OpenAPI allows you to define validation schemas for the API's inputs and outputs. This ensures that the data sent and received meets the expected formats, reducing errors and improving the robustness of the API.

- **Security**: The OpenAPI specification allows you to define security schemes, such as authentication and authorization, which help ensure that the API is protected against unauthorized access.

In summary, using a schema like OpenAPI to document the inputs and outputs of an API provides clarity, facilitates collaboration, improves maintainability and security, and allows you to leverage advanced tools for testing and code generation.

## OpenAPI

OpenAPI specifies a standard for defining and describing APIs. With OpenAPI, you can create clear and detailed documentation that describes the endpoints, HTTP methods, parameters, responses, and other elements of your API. This makes it easier for other developers to understand and use the API.

## Swagger

Swagger is a set of tools built around the OpenAPI specification. It includes Swagger UI, which provides an interactive graphical interface for testing and exploring APIs.

## Integration

To enable integration with OpenAPI and Swagger, you just need to activate them.

```python
from cafeto import App
from cafeto.mvc import BaseController


app: App = App(debug=True)

@app.controller()
class UserController(BaseController):
    @app.post('/create')
    async def create(self, data: CreateUserRequestDto) -> CreateUserResponseDto:
        # My code here

app.map_controllers()
app.use_schema()
if app.debug:
    app.use_swagger()
```

There are two entry points to view the OpenAPI documentation in `json` and `yaml` format:

- [http://127.0.0.1:8000/schema/openapi.json](http://127.0.0.1:8000/schema/openapi.json)
- [http://127.0.0.1:8000/schema/openapi.yaml](http://127.0.0.1:8000/schema/openapi.yaml)

And to view the Swagger UI interface, go to:

- [http://127.0.0.1:8000/schema/swagger-ui.html](http://127.0.0.1:8000/schema/swagger-ui.html)

## Documentation

The OpenAPI documentation will be automatically created using the actions of the controllers as the data source. Relevant information includes output data (the response of the actions) and input data, including request parameters such as `path`, `query string`, `headers`, and the data they return. It will also consider if the actions have access control with the `@app.requires` decorator.

It is also a good idea to provide general documentation about the API.

```python
from cafeto import SecurityScheme, Info, Contact, License, ExternalDocs


security_scheme: SecurityScheme = SecurityScheme(
    name='auth',
    bearer_format='JWT',
    type='http',
    scheme='bearer'
)

info: Info = Info(
    title='My API',
    description='Lorem ipsum dolor sit amet, consectetuer adipiscing elit.',
    version='1.0.0',
    terms_of_service='http://my_api_terms_of_service.html',
    contact=Contact(
        name='Cafeto',
        url='http://my_api_contact.html',
        email='my_api@email.com'
    ),
    license=License(
        name='My License',
        url='http://my_license.html'
    )
)

external_docs: ExternalDocs = ExternalDocs(
    description='Find more info here',
    url='http://my_docs.html'
)

app.use_schema(
    openapi_version='3.0.1', # Default
    info=info,
    security_scheme=security_scheme,
    external_docs=external_docs
)
```

It is possible to add additional documentation to controllers and actions using Python docstrings.

```python
@app.controller()
class HomeController(BaseController):
    '''
    description: Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
    '''
    @app.get('/hello')
    async def hello(self) -> UserResponseDto:
        '''
        summary: Lorem ipsum.
        description: Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
        responses:
            200:
                default: true
                description: Lorem ipsum
            400:
                description: Lorem ipsum
        '''
```

The format used for this documentation is `yml`. In the action documentation, in the `responses` section, there is the `default` option. If this is set to `true`, it means that this response corresponds to the data that the action will return.
