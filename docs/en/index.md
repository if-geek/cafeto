# Cafeto

## Introduction

Cafeto is a lightweight yet powerful framework designed as a top layer over [Starlette](https://www.starlette.io/), focusing on simplifying and accelerating the development of modern APIs. It harnesses the robust foundation of [Starlette](https://www.starlette.io/), offering additional tools for more efficient and organized development.

[:flag_us: English](/cafeto) | [:flag_co: Español](/cafeto/es)

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
import uvicorn

from cafeto import App
from cafeto.mvc import BaseController
from cafeto.responses import Ok
from cafeto.models import BaseModel


app: App = App()

class CreateUserRequestDto(BaseModel):
    username: str
    password: str


class CreateUserResponseDto(BaseModel):
    id: int
    username: str


@app.controller('/user')
class UserController(BaseController):
    @app.post('/create')
    async def create(self, data: CreateUserRequestDto) -> CreateUserResponseDto:
        user = {'id': 1, 'username': data.username}
        return Ok(CreateUserResponseDto(**user))

app.map_controllers()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
```

1. It can also be run by command:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

This example shows how to define a controller and two DTOs (one for the request and one for the response), and how to set up a route to create a user.

The `App` class inherits from the `Starlette` class, which means that the properties of Starlette are also available in the App class. An example of these properties is `Middleware`. However, there is an additional configuration called `CafetoConfig`, which will be explained later.

```python
from cafeto.middleware import CORSMiddleware

middleware = [
    Middleware(CORSMiddleware, allow_origins=['*'])
]

app: App = App(debug=True, middleware=middleware)
```

## Conclusion

Cafeto is a powerful tool that facilitates the creation of APIs in Python. With support for dependency injection, DTOs, and automatic documentation, it is an excellent choice for developers looking for a simple yet professional solution for their API projects.
