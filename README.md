# Cafeto

Cafeto is a lightweight yet powerful framework designed as a top layer over [Starlette](https://www.starlette.io/), focusing on simplifying and accelerating the development of modern APIs. It harnesses the robust foundation of [Starlette](https://www.starlette.io/), offering additional tools for more efficient and organized development.

## Requirements

This project requires **Python 3.10** or a later version.

## Installation

```bash
pip install cafeto
```

## Project

[Cafeto](https://github.com/if-geek/cafeto/)

## Docs

[Cafeto docs](https://if-geek.github.io/cafeto/)

## Example Project

[Cafeto Example](https://github.com/if-geek/cafeto_example)

## Description

Cafeto is a framework designed to create APIs efficiently and in an organized manner, drawing inspiration from other frameworks while incorporating innovative ideas.

- It offers a robust dependency injection system, supporting three lifecycle types: `Singleton`, `Scoped`, and `Transient`.
- Facilitates the handling of incoming and outgoing data through DTOs (Data Transfer Objects), which also play a key role in validating and managing server interactions.
- Includes an event system that extends the framework's capabilities, enabling greater customization and flexibility.
- Integrates seamlessly with tools like OpenAPI and Swagger to provide interactive documentation and API testing.

With Cafeto, developers can build scalable and reliable APIs effortlessly, leveraging modern features and a well-structured approach.

## Starlette

Starlette, the backbone of Cafeto, is widely recognized as one of the most outstanding frameworks for building asynchronous web applications in Python. Its minimalist design, coupled with exceptional performance, makes it ideal for developers seeking flexibility and power. Starlette not only provides routing, middleware, and WebSocket support but also integrates advanced tools for asynchronous task management and testing, establishing itself as a gold standard in modern web development.

Building on Starlette’s power, Cafeto takes the experience to the next level, delivering an even more streamlined and developer-friendly solution for API creation. Together, Cafeto and Starlette form the perfect duo for any developer seeking speed, simplicity, and technical excellence.

## Main Objective

To create a smoother development experience for APIs, providing intuitive abstractions, smart default configurations, and compatibility with modern standards.

## Example

```python
from typing import Dict

from cafeto import App
from cafeto.mvc import BaseController
from cafeto.responses import Ok


app: App = App()

@app.controller('/home')
class HomeController(BaseController):
    @app.get('/hello')
    async def hello(self, name: str) -> Dict[str, str]:
        return Ok({'Hello': 'World!'})

app.map_controllers()

```

For more usage details, see the [features](https://if-geek.github.io/cafeto/)


## License

This project is licensed under the [MIT License](LICENSE)

## Contact

Jonathan Espinal - jonathan.espinal@gmail.com

## Documentation

[Features](docs/FEATURES.md)

[Next Steps](docs/NEXT_STEPS.md)
