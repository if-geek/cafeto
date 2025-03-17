import os
from typing import Any, Callable, Dict, List, Optional, Sequence, Type, overload
import typing

import yaml

from starlette.responses import PlainTextResponse, HTMLResponse, JSONResponse
from starlette.applications import Starlette
from starlette.types import ExceptionHandler, Lifespan
from starlette.applications import AppType

from jinja2 import Environment, PackageLoader, select_autoescape

from cafeto.models import BaseModel
from cafeto.events import OnAfterAction, OnBeforeAction, OnExecuteAction
from cafeto.routing import BaseRoute
from cafeto.middleware import Middleware
from cafeto.services import ContextService, AContextService
from cafeto.staticfiles import StaticFiles
from cafeto.dependency_injection.service_collection import Dependencies, ServiceCollection
from cafeto.dependency_injection.service_provider import ServiceProvider
from cafeto.mvc.action import create_endpoint
from cafeto.mvc.base_controller import BaseController
from cafeto.requests import Request
from cafeto.schema.library.schema import ExternalDocs, Info, SecurityScheme
from cafeto.mvc.endpoint import Endpoint
from cafeto.authentication.requires import Requires
from cafeto.mvc.types import Action
from cafeto.dependency_injection.service_provider import scoped_copy_var


class CafetoConfig:
    def __init__(
            self,
            error_object: bool = False,
            error_list_key: str = 'errorList',
            error_object_key: str = 'errorObject'
            ):
        self.error_object: bool = error_object
        self.error_list_key: str = error_list_key
        self.error_object_key: str = error_object_key


class App(Starlette):

    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(App, cls).__new__(cls)
        return cls.instance

    def __init__(
        self: AppType,
        debug: bool = False,
        routes: typing.Sequence[BaseRoute] | None = None,
        middleware: typing.Sequence[Middleware] | None = None,
        exception_handlers: typing.Mapping[typing.Any, ExceptionHandler] | None = None,
        on_startup: typing.Sequence[typing.Callable[[], typing.Any]] | None = None,
        on_shutdown: typing.Sequence[typing.Callable[[], typing.Any]] | None = None,
        lifespan: Lifespan[AppType] | None = None,
        config: CafetoConfig = CafetoConfig(),
    ) -> None:
        super().__init__(
            debug=debug,
            routes=routes,
            middleware=middleware,
            exception_handlers=exception_handlers,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            lifespan=lifespan
            )
        self.config: CafetoConfig = config
        self.action_list: List[Action] = []
        self.action_list_tmp: List[Action] = []
        self.schema = {
            'components': None,
            'tags': None
        }

        self.start()

    def start(self) -> None:
        ServiceProvider.instance = None
        ServiceCollection.instance = None
        ServiceProvider()
        ServiceCollection.clear()

        OnBeforeAction.clear()
        OnExecuteAction.clear()
        OnAfterAction.clear()

    def map_controllers(self) -> None:
        """
        Maps actions to the given Starlette application by adding routes.

        This function iterates over a list of actions defined in the Action class,
        applies each action to get the corresponding endpoint, and adds a route
        to the Starlette application with the specified path and HTTP method.
        Returns:
            None
        """

        for action in self.action_list:
            endpoint = create_endpoint(action)
            if action.endpoint.method == 'WEBSOCKET':
                self.add_websocket_route(action.endpoint.path, endpoint)
            else:
                self.add_route(action.endpoint.path, endpoint, methods=[action.endpoint.method])

    def use_schema(
            self,
            openapi_version: str = '3.0.1',
            info: Optional[Info] = None,
            security_scheme: Optional[SecurityScheme] = None,
            external_docs: Optional[ExternalDocs] = None
            ) -> None:
        """
        Integrates OpenAPI schema generation into a Starlette application.
        This function creates an OpenAPI schema for the given Starlette application
        and sets up routes to serve the schema in both JSON and YAML formats.
        Returns:
            None
        Routes:
            /schema/openapi.json: Returns the OpenAPI schema in JSON format.
            /schema/openapi.yaml: Returns the OpenAPI schema in YAML format.
        """

        from cafeto.schema.openapi import create_schema

        schema = create_schema(self, openapi_version, info, security_scheme, external_docs)

        async def openapi_json(request: Request) -> JSONResponse:
            return JSONResponse(schema)

        async def openapi_yaml(request: Request) -> PlainTextResponse:
            return PlainTextResponse(yaml.dump(schema, sort_keys=False, indent=2))

        self.add_route("/schema/openapi.json", openapi_json, methods=["GET"])
        self.add_route("/schema/openapi.yaml", openapi_yaml, methods=["GET"])

    def use_swagger(self) -> None:
        """
        Integrates Swagger UI into a Starlette application.
        This function sets up the necessary routes and static file serving to enable
        Swagger UI for API documentation. It mounts the static files required for
        Swagger UI and adds a route to serve the Swagger UI HTML page.
        Args:
            app (Starlette): The Starlette application instance to which Swagger UI
                            will be added.
        Returns:
            None
        """
        env = Environment(loader=PackageLoader("cafeto"), autoescape=select_autoescape(["html", "xml"]))

        async def swagger(request: Request) -> HTMLResponse:
            template = env.get_template('cafeto/swagger.html')
            content = template.render(url='/schema/openapi.yaml')
            return HTMLResponse(content)

        current_file_directory = os.path.dirname(__file__)
        static_files_directory = os.path.join(current_file_directory, "static")

        self.mount("/static", StaticFiles(directory=static_files_directory), name="static_cafeto")
        self.add_route("/schema/swagger-ui.html", swagger, methods=["GET"])

    def get(
            self,
            path: str,
            query: Optional[Sequence[str]] = [],
            headers: Optional[Sequence[str]] = [],
            body: Optional[Dict[str, Any]] = {}
            ):
        def decorator(action: Action) -> Action:
            self.__set_action(action, path, "GET", query, headers, body)
            return action
        return decorator

    def post(
            self,
            path: str,
            query: Optional[Sequence[str]] = [],
            headers: Optional[Sequence[str]] = [],
            body: Optional[Dict[str, Any]] = {}
            ):
        def decorator(action: Action) -> Action:
            self.__set_action(action, path, "POST", query, headers, body)
            return action
        return decorator

    def put(
            self,
            path: str,
            query: Optional[Sequence[str]] = [],
            headers: Optional[Sequence[str]] = [],
            body: Optional[Dict[str, Any]] = {}
            ):
        def decorator(action: Action) -> Action:
            self.__set_action(action, path, "PUT", query, headers, body)
            return action
        return decorator

    def delete(
            self,
            path: str,
            query: Optional[Sequence[str]] = [],
            headers: Optional[Sequence[str]] = [],
            body: Optional[Dict[str, Any]] = {}
            ):
        def decorator(action: Action) -> Action:
            self.__set_action(action, path, "DELETE", query, headers, body)
            return action
        return decorator

    def patch(
            self,
            path: str,
            query: Optional[Sequence[str]] = [],
            headers: Optional[Sequence[str]] = [],
            body: Optional[Dict[str, Any]] = {}
            ):
        def decorator(action: Action) -> Action:
            self.__set_action(action, path, "PATCH", query, headers, body)
            return action
        return decorator

    def websocket(
            self,
            path: str,
            query: Optional[Sequence[str]] = [],
            headers: Optional[Sequence[str]] = [],
            body: Optional[Dict[str, Any]] = {}
            ):
        def decorator(action: Action) -> Action:
            self.__set_action(action, path, "WEBSOCKET", query, headers, body)
            return action
        return decorator

    def requires(self, scope: str | list[str], status_code: int = 403, redirect: str | None = None):
        def decorator(action: Action) -> Action:
            self.__set_requires(action, scope, status_code, redirect)
            return action
        return decorator

    def __get_default_values(self, action: Action):
        """
        Extracts the default values of parameters from a given action.
        Args:
            action (Action): The action from which to extract parameter default values.
                            This is expected to be a function or callable with annotations,
                            defaults, and keyword defaults.
        Returns:
            dict: A dictionary where keys are parameter names and values are their default values.
                If a parameter does not have a default value, its value in the dictionary will be None.
        """
        annotations = action.__annotations__
        defaults = action.__defaults__
        param_names = action.__code__.co_varnames

        param_defaults = {}

        if defaults:
            positional_params_with_defaults = param_names[-len(defaults):]
            for param, value in zip(positional_params_with_defaults, defaults):
                param_defaults[param] = value

        result = {}
        for param, _ in annotations.items():
            default_value = param_defaults.get(param, None)
            result[param] = default_value

        return result

    def __set_action(
            self,
            action: Action,
            path: str,
            method: str,
            query: Optional[Sequence[str]] = [],
            headers: Optional[Sequence[str]] = [],
            body: Optional[Dict[str, Any]] = {}
            ) -> None:
        App.__set_endpoint_property(action)
        default_values = self.__get_default_values(action)
        action.endpoint = Endpoint(path, method, query, headers, body, default_values)
        self.action_list_tmp.append(action)

    def __set_requires(
            self,
            action: Action,
            scope: str | list[str],
            status_code: int = 403,
            redirect: str | None = None
            ) -> None:
        App.__set_requires_property(action)
        action.requires = Requires(scope, status_code, redirect)

    @staticmethod
    def __set_endpoint_property(action: Action) -> None:
        if not hasattr(action, 'endpoint'):
            setattr(action, 'endpoint', None)

    @staticmethod
    def __set_requires_property(action: Action) -> None:
        if not hasattr(action, 'requires'):
            setattr(action, 'requires', None)

    def controller(self, path: Optional[str] = None) -> Callable[[Type[BaseController]], Type[BaseController]]:
        def decorator(cls: Type[BaseController]) -> Type[BaseController]:
            path_url = path
            if path_url is None or path_url == '':
                path_url = '/' + cls.__name__.lower().replace('controller', '')

            for action in self.action_list_tmp:
                action.endpoint.path = path_url + action.endpoint.path
                action.endpoint.controller = cls
                self.action_list.append(action)
            self.action_list_tmp.clear()
            return cls
        return decorator

    @overload
    def add_singleton(self, implementation: Type, *, override: bool = False):  # pragma: no cover
        ...

    @overload
    def add_singleton(self, dep_type: Type, implementation: Type, *, override: bool = False):  # pragma: no cover
        ...

    @overload
    def add_singleton(self, implementation: Type, generator: Callable, *, override: bool = False):  # pragma: no cover
        ...

    @overload
    def add_singleton(
        self,
        dep_type: Type,
        implementation: Type,
        generator: Callable,
        *,
        override: bool = False
    ):  # pragma: no cover
        ...

    def add_singleton(
            self,
            dep_type: Type,
            implementation: Optional[Type] = None,
            generator: Callable = None,
            *,
            override: bool = False
            ):  # pragma: no cover
        ServiceCollection.add_singleton(dep_type, implementation, generator, override=override)

    def remove_singleton(self, dep_type: Type) -> None:
        ServiceCollection.remove_singleton(dep_type)

    @overload
    def add_scoped(self, implementation: Type, *, override: bool = False):  # pragma: no cover
        ...

    @overload
    def add_scoped(self, dep_type: Type, implementation: Type, *, override: bool = False):  # pragma: no cover
        ...

    @overload
    def add_scoped(self, implementation: Type, generator: Callable, *, override: bool = False):  # pragma: no cover
        ...

    @overload
    def add_scoped(
        self,
        dep_type: Type,
        implementation: Type,
        generator: Callable,
        *,
        override: bool = False
    ):  # pragma: no cover
        ...

    def add_scoped(
            self,
            dep_type: Type,
            implementation: Optional[Type] = None,
            generator: Callable = None,
            *,
            override: bool = False
            ):  # pragma: no cover
        ServiceCollection.add_scoped(dep_type, implementation, generator, override=override)

    def remove_scoped(self, dep_type: Type) -> None:
        ServiceCollection.remove_scoped(dep_type)

    @overload
    def add_transient(self, implementation: Type, *, override: bool = False):  # pragma: no cover
        ...

    @overload
    def add_transient(self, dep_type: Type, implementation: Type, *, override: bool = False):  # pragma: no cover
        ...

    @overload
    def add_transient(self, implementation: Type, generator: Callable, *, override: bool = False):  # pragma: no cover
        ...

    @overload
    def add_transient(
        self,
        dep_type: Type,
        implementation: Type,
        generator: Callable,
        *,
        override: bool = False
    ):  # pragma: no cover
        ...

    def add_transient(
            self,
            dep_type: Type,
            implementation: Optional[Type] = None,
            generator: Callable = None,
            *,
            override: bool = False
            ):  # pragma: no cover
        ServiceCollection.add_transient(dep_type, implementation, generator, override=override)

    def remove_transient(self, dep_type: Type) -> None:
        ServiceCollection.remove_transient(dep_type)

    def use_default_services(self) -> None:
        self.add_scoped(AContextService, ContextService)

        def populate_context_service_action(controller: BaseController, action: Action, data: BaseModel) -> None:
            scoped: Dependencies = scoped_copy_var.get()
            if scoped is None:  # pragma: no cover
                return

            context_service = scoped.get(AContextService, None)
            if context_service is not None and context_service.value is not None:

                headers = {}
                query = {}
                if controller.request is not None:
                    headers = dict(controller.request.headers.items())
                    query = dict(controller.request.query_params.items())
                elif controller.websocket is not None:  # pragma: no cover
                    headers = dict(controller.websocket.headers.items())
                    query = dict(controller.websocket.query_params.items())

                context_service.value.set_data(
                    action.endpoint.path,
                    action.endpoint.method,
                    headers,
                    query,
                    controller.__class__.__name__,
                    action.__name__,
                    data
                )

        OnExecuteAction.add(populate_context_service_action)
