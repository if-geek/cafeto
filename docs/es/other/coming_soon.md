# Próximamente

## Introducción

Aunque el sistema ya es muy efectivo y ofrece un conjunto sólido de características, se está trabajando continuamente para mejorarlo. El objetivo es seguir implementando nuevas mejoras y funcionalidades para optimizar la experiencia del usuario. Aquí tienes algunas de las emocionantes actualizaciones que se pueden esperar:

## Inyección de dependencias desde el constructor del controlador

Permitir que las acciones que comparten dependencias no necesiten definirlas en cada acción del mismo controlador.

Ejemplo:

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

## Mejoras en la funcionalidad de los eventos

Optimizar el sistema de eventos para hacerlo más versátil y robusto, incorporando características como:

- Permitir que los eventos generen respuestas, facilitando una interacción más dinámica.

- Implementar la capacidad de lanzar excepciones desde los eventos, con soporte para que estas puedan ser capturadas e interceptadas según sea necesario.

- Asegurar un manejo eficiente de errores y un flujo controlado en la ejecución de los eventos.

## Incorporación de nuevos eventos

Extender el sistema actual con la adición de nuevos eventos. Algunas ideas iniciales incluyen:

- **OnModeValidationFail**: Evento desencadenado cuando la validación de un modo falla, permitiendo gestionar este caso de manera específica y personalizada.

## Sistema mejorado de validaciones

Implementaremos un sistema más avanzado para la validación de datos.

La idea general es crear un sistema de validaciones que se pueda usar fuera de los DTOs y ofrecer una forma fácil de retornar errores en caso de existir.

### Objetivos
- **Flexibilidad**: Permitir el uso de validaciones en diferentes contextos más allá de los DTOs.
- **Facilidad de uso**: Proveer una interfaz sencilla para la definición y el manejo de reglas de validación.
- **Eficiencia**: Garantizar que las validaciones se realicen de manera rápida y efectiva.

## Implementación de CLI

Desarrollaremos una interfaz de línea de comandos (CLI) para la creación de proyectos.

### Ejemplos

1. **Crear un nuevo proyecto**:
```bash
cafeto new project-name
```

1. **Generar un controlador**:
```bash
cafeto create controller user
```

### Objetivos

- **Facilidad de uso**: Proveer comandos sencillos e intuitivos para la creación y gestión de proyectos.

- **Eficiencia**: Reducir el tiempo y esfuerzo necesarios para inicializar y configurar proyectos.

- **Flexibilidad**: Permitir la extensión y personalización de la CLI según las necesidades del usuario.

## Plantillas de desarrollo

Dotaremos al sistema con la capacidad de iniciar proyectos con plantillas predefinidas, evitando comenzar desde cero en cada nuevo proyecto.

## Sistema de usuarios y permisos por defecto

Desarrollaremos un sistema en el cual la gestión de usuarios y permisos estará prediseñada, permitiendo ahorrar tiempo en cada nuevo proyecto.

## Mejoras en la documentación

Estamos trabajando en mejorar la documentación, añadiendo más ejemplos y proporcionando más detalles sobre las características del sistema.

## Incrementar el soporte a los parámetros

Añadir la capacidad de soportar otros tipos de datos más complejos como listas, fechas, etc.

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

## Mejorar la integración con OpenApi

Daremos más soporte a las características de OpenApi para mejorar la integración.

## Integración con Prometheus y Grafana

Con el sistema de plantillas y usando Docker, se implementará la capacidad de crear logs de los eventos del API para generar métricas del sistema. Esta integración permitirá a los desarrolladores y administradores de sistemas monitorear el rendimiento y la salud de sus aplicaciones de manera más efectiva.

### Objetivos

- **Monitoreo en tiempo real**: Permitir la observación en tiempo real de las métricas del sistema, como el uso de CPU, memoria, latencia de las solicitudes, tasas de error, entre otros.
- **Alertas proactivas**: Configurar alertas que notifiquen a los administradores cuando ciertos umbrales críticos sean alcanzados, permitiendo una respuesta rápida a posibles problemas.
- **Análisis histórico**: Almacenar datos históricos para analizar tendencias y patrones de uso a lo largo del tiempo, ayudando en la toma de decisiones informadas sobre la infraestructura y el rendimiento de la aplicación.
- **Visualización de datos**: Utilizar Grafana para crear dashboards personalizados que visualicen las métricas recolectadas de manera clara y comprensible.

## Respuestas en estilos personalizados

Permitir elegir entre diferentes estilos de respuesta para los servicios, no limitándose únicamente a JSON. La idea es poder cambiar entre `JSON`, `XML` y `YML`.

=== "Estilo unificado"
    ```python
    from cafeto.responses import Ok

    @app.controller()
    class UserController(BaseController):
        @app.get('/view/{id}')
        async def view(self, id: int) -> UserResponseDto:
            user = <some_user_service>.get(id)
            return Ok(UserResponseDto(**user), style='XML')
    ```

=== "Estilo clasico"
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
    **estilos**

    - style='JSON' (default)
    - style='XML'
    - style='YML'

## Mejoras de rendimiento

Optimizaremos el sistema para asegurar un rendimiento más rápido y eficiente.

## Creación de un prefijo para el API

Se propone la funcionalidad de agregar un prefijo a las URLs de todos los endpoints de la API para mantener una estructura más organizada y consistente.

Por ejemplo, utilizando el siguiente comando:

```python
app.map_controllers(prefix='my-api')
```

Esto garantizará que todas las rutas de los servicios comiencen con el prefijo especificado. El resultado sería algo como:

```bash
http://127.0.0.1:8000/my-api/my-controller/my-action
```

De esta forma, se facilita la agrupación de endpoints bajo un mismo contexto y se mejora la legibilidad y administración de las rutas dentro de la API.

## Sistema de versionamiento de las APIs

Implementar un sistema de versionamiento para las APIs que permitirá a los desarrolladores gestionar y mantener múltiples versiones de sus APIs de manera eficiente.

### Objetivos

- **Compatibilidad**: Asegurar que las versiones anteriores de las APIs sigan funcionando mientras se desarrollan nuevas versiones.
- **Facilidad de uso**: Proveer herramientas y documentación clara para la gestión de versiones.
- **Flexibilidad**: Permitir a los desarrolladores elegir qué versiones de las APIs desean mantener y cuáles descontinuar.

### Ejemplo

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
       **Otra manera**
       
       ```python
       @app.controller() # 'v2' by default
       ```

## Adaptabilidad y evolución continua

Nos comprometemos con la mejora continua y la adaptación a las novedades del entorno tecnológico. El proyecto está en constante evolución, observando las tendencias y avances en el ámbito del desarrollo de software para implementar las mejores prácticas y tecnologías más recientes.

La meta es asegurarse de que el sistema permanezca actualizado y relevante, incorporando nuevas características y optimizaciones que beneficien a los usuarios. Se agradecen las sugerencias y siempre estamos abiertos a recibir feedback para seguir mejorando.

### Ejemplo

- **Integración de nuevas tecnologías:** Adoptar nuevas herramientas y frameworks que emergen en el mercado.
- **Actualizaciones regulares:** Implementar mejoras y parches de seguridad de manera continua.
- **Feedback del usuario:** Escuchar activamente las necesidades y sugerencias de los usuarios para adaptarse a sus requerimientos.
