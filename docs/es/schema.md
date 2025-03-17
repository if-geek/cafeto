# Esquema

## Introducción

Usar un esquema como OpenAPI para mostrar las entradas y salidas de una API ofrece varias ventajas significativas:

- **Documentación clara y detallada**: OpenAPI permite crear una documentación exhaustiva que describe los endpoints, métodos HTTP, parámetros, respuestas y otros elementos de la API. Esto facilita la comprensión y el uso de la API por parte de otros desarrolladores.

- **Facilita la colaboración**: Con una documentación bien definida, los equipos de desarrollo pueden colaborar de manera más efectiva. Los desarrolladores pueden entender rápidamente cómo interactuar con la API, lo que reduce la necesidad de comunicación adicional.

- **Pruebas y depuración más sencillas**: Herramientas como Swagger UI proporcionan una interfaz gráfica interactiva para probar y explorar las APIs. Esto permite a los desarrolladores y testers verificar rápidamente el funcionamiento de los endpoints y detectar posibles errores.

- **Estandarización**: OpenAPI sigue un estándar reconocido para definir y describir APIs. Esto asegura que la documentación sea consistente y comprensible, independientemente de quién la haya creado.

- **Generación automática de código**: Muchas herramientas pueden generar automáticamente código cliente y servidor a partir de una especificación OpenAPI. Esto acelera el desarrollo y asegura que el código generado esté alineado con la documentación.

- **Mejora la mantenibilidad**: Tener una documentación actualizada y precisa facilita el mantenimiento de la API. Los cambios en los endpoints, parámetros o respuestas se pueden reflejar rápidamente en la documentación, asegurando que todos los usuarios de la API estén al tanto de las modificaciones.

- **Validación de datos**: OpenAPI permite definir esquemas de validación para las entradas y salidas de la API. Esto asegura que los datos enviados y recibidos cumplan con los formatos esperados, reduciendo errores y mejorando la robustez de la API.

- **Seguridad**: La especificación OpenAPI permite definir esquemas de seguridad, como autenticación y autorización, lo que ayuda a asegurar que la API esté protegida contra accesos no autorizados.

En resumen, usar un esquema como OpenAPI para documentar las entradas y salidas de una API proporciona claridad, facilita la colaboración, mejora la mantenibilidad y seguridad, y permite aprovechar herramientas avanzadas para pruebas y generación de código.

## OpenAPI

OpenAPI especifica un estándar para definir y describir APIs. Con OpenAPI, puedes crear una documentación clara y detallada que describe los endpoints, métodos HTTP, parámetros, respuestas y otros elementos de tu API. Esto facilita la comprensión y el uso de la API por parte de otros desarrolladores.

## Swagger

Swagger es un conjunto de herramientas creadas en torno a la especificación OpenAPI. Incluye Swagger UI, que proporciona una interfaz gráfica interactiva para probar y explorar las APIs.

## Integración

Para activar la integración con OpenApi y Swagger, solo necesitas activarlos.

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

Existen dos puntos de entrada para ver la documentación en OpenApi en formato `json` y `yaml`:

- [http://127.0.0.1:8000/schema/openapi.json](http://127.0.0.1:8000/schema/openapi.json)
- [http://127.0.0.1:8000/schema/openapi.yaml](http://127.0.0.1:8000/schema/openapi.yaml)

Y para ver la interfaz de Swagger UI, accede a:

- [http://127.0.0.1:8000/schema/swagger-ui.html](http://127.0.0.1:8000/schema/swagger-ui.html)

## Documentación

La documentación OpenApi se creará de forma automática tomando como fuente de datos las acciones de los controladores. Entre la información relevante se incluyen los datos de salida (la respuesta de las acciones) y los datos de entrada, tanto de los request como los parámetros `path`, `querystring`, `headers` y los datos que retornan. También se tomará en cuenta si las acciones tienen control de acceso con el decorador `@app.requires`.

También es una buena idea proporcionar documentación general sobre la API.

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
    openapi_version='3.0.1', # Por defecto
    info=info,
    security_scheme=security_scheme,
    external_docs=external_docs
)
```

Es posible agregar documentación adicional a los controladores y acciones usando docstrings de Python.

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

El formato utilizado para esta documentación es `yml`. En la documentación de la acción, en la sección `responses`, existe la opción `default`. Si esta está en `true`, quiere decir que esta respuesta es la que corresponde al dato que retornará la acción.
