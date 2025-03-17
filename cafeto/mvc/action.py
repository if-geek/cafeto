from typing import Any, Awaitable, Callable, Optional, Dict, Type, Union

from starlette.responses import JSONResponse
from starlette.authentication import requires as requires_starlette
from starlette.websockets import WebSocket as StarletteWebSocket

from cafeto.convertors import CONVERTOR_TYPES
from cafeto.datastructures import UploadFile
from cafeto.dependency_injection.service_provider import ServiceProvider
from cafeto.models.base_model import BaseModel
from cafeto.events import OnAfterAction, OnBeforeAction, OnExecuteAction
from cafeto.responses import BaseResponse, Response
from cafeto.requests.request import get_request_body_model
from cafeto.errors.errors import ParamConvertError, RequestError
from cafeto.mvc.types import Action
from cafeto.mvc import Request, WebSocket


def create_endpoint(action: Action) -> Callable[[Action], Callable[[Request], Awaitable[Any]]]:
    """
    Creates an endpoint for the given action.

    Args:
        action (Action): The action for which the endpoint is being created.

    Returns:
        Callable[[Action], Callable[[Request], Awaitable[Any]]]: A callable that takes an action and returns an
        asynchronous callable that takes a request and returns an awaitable result.

    The endpoint function handles both HTTP requests and WebSocket connections based on the action's endpoint method.
    If the action requires specific conditions (e.g., authentication), these are applied to the endpoint.
    """

    endpoint = _get_endpoint(action)

    if hasattr(action, 'requires') and action.requires is not None:
        endpoint = requires_starlette(
            action.requires.scope,
            status_code=action.requires.status_code,
            redirect=action.requires.redirect
        )(endpoint)

    return endpoint


def _get_endpoint(action: Action) -> Callable[[Action], Callable[[Request], Awaitable[Any]]]:
    """
    Returns an endpoint function based on the action's endpoint method.

    Args:
        action (Action): The action object containing endpoint information.

    Returns:
        Callable[[Action], Callable[[Request], Awaitable[Any]]]:
        A function that takes a Action and returns an asynchronous function
        that handles either HTTP requests or WebSocket connections.
    """
    async def endpoint_request(request: Request) -> Callable[[Request], Awaitable[Any]]:
        copy_request = Request(request)
        del request
        return await _endpoint(action, copy_request)

    async def endpoint_websocket(websocket: StarletteWebSocket) -> Callable[[WebSocket], Awaitable[Any]]:
        copy_websocket = WebSocket(websocket)
        del websocket
        return await _endpoint(action, copy_websocket)

    if action.endpoint.method == 'WEBSOCKET':
        return endpoint_websocket
    return endpoint_request


def _convert_param(param_value: str, param_type: Type) -> Any:
    """
    Converts a parameter value to the specified type using a predefined set of converters.
    The converter use Starlette CONVERTOR_TYPES to convert the parameter value to the specified type.

    Args:
        param_value (str): The parameter value to be converted.
        param_type (Type): The type to which the parameter value should be converted.

    Returns:
        Any: The converted parameter value.

    Raises:
        ParamConvertError: If no converter is found for the specified type.
    """
    convertor_name = str(param_type.__name__).lower()
    if convertor_name in CONVERTOR_TYPES:
        return CONVERTOR_TYPES[convertor_name].convert(param_value)
    raise ParamConvertError(param_value, param_type)  # pragma: no cover


async def _get_query_param(request: Request, param_name: str, param_type: Type, default_values: Dict[str, Any]) -> Any:
    """
    Asynchronously retrieves a query parameter from the request.

    Args:
        request (Request): The incoming request object.
        param_name (str): The name of the query parameter to retrieve.
        param_type (Type): The expected type of the query parameter.
        default_values (Dict[str, Any]): A dictionary of default values for query parameters.

    Returns:
        Any: The value of the query parameter, converted to the specified type, or the default value if the parameter
        is not present in the request.
    """
    if param_name in request.query_params:
        return _convert_param(request.query_params[param_name], param_type)
    return default_values.get(param_name, None)


async def _get_header_param(request: Request, param_name: str, param_type: Type, default_values: Dict[str, Any]) -> Any:
    """
    Asynchronously retrieves a header parameter from the request and converts it to the specified type.

    Args:
        request (Request): The incoming request object.
        param_name (str): The name of the header parameter to retrieve.
        param_type (Type): The type to which the header parameter should be converted.
        default_values (Dict[str, Any]): A dictionary of default values for parameters.

    Returns:
        Any: The converted header parameter value if it exists, otherwise the default value for the parameter.
    """
    if param_name in request.headers:
        return _convert_param(request.headers[param_name], param_type)
    return default_values.get(param_name, None)


async def _get_upload_file(request: Request, param_name: str) -> Any:
    """
    Asynchronously retrieves an uploaded file from a request.

    Args:
        request (Request): The incoming HTTP request containing the form data.
        param_name (str): The name of the parameter to retrieve from the form data.

    Returns:
        Any: The uploaded file from the form data.
    """
    form = await request.form()
    return form['file']


async def _endpoint(
        action: Action,
        request: Union[Request, WebSocket]
        ) -> Callable[[Request], Awaitable[Any]]:
    """
    Asynchronous endpoint handler that resolves dependencies and invokes the appropriate controller action.
    This method is the actual method called by Starlette when a request is received. It calls the action method
    in the controller and returns the response.


    Args:
        action (Action): The action to be executed, containing endpoint and annotations.
        request (Request | StarletteWebSocket): The incoming request or WebSocket connection.

    Returns:
        Callable[[Request], Awaitable[Any]]: A callable that takes a request and returns an awaitable result.

    Raises:
        JSONResponse: If there is a ModelError during request data processing, returns a JSON response with
        error details.
    """
    controller = action.endpoint.controller()
    action_method = controller.__getattribute__(action.__name__)
    if isinstance(request, WebSocket):
        controller.websocket = request
    else:
        controller.request = request
    params: Dict[str, Type] = action.__annotations__

    token = ServiceProvider.scoped_copy()

    # Execute on_before action event
    await OnBeforeAction.execute(controller, action)

    params_to_send: Optional[Dict[str, Any]] = ServiceProvider.resolve(action)

    if isinstance(request, WebSocket):
        request.body = action.endpoint.body

    default_values: Dict[str, Any] = action.endpoint.default_values
    request_model: BaseModel = None

    for param_name, param_type in params.items():
        if param_name == 'return' or param_name in params_to_send:
            continue

        if param_name in request.path_params:
            params_to_send[param_name] = _convert_param(request.path_params[param_name], param_type)
            continue

        if param_name in action.endpoint.query:
            params_to_send[param_name] = await _get_query_param(request, param_name, param_type, default_values)
            continue

        if param_name in action.endpoint.headers:
            params_to_send[param_name] = await _get_header_param(request, param_name, param_type, default_values)
            continue

        if param_type == UploadFile:
            params_to_send[param_name] = await _get_upload_file(request, param_name)
            continue

        try:
            request_body = await request.json()
            request_model = await get_request_body_model(request_body, param_type, action.endpoint.body)
        except RequestError as e:
            ServiceProvider.reset_scoped(token)
            return JSONResponse(e.errors, status_code=400)

        params_to_send[param_name] = request_model

    # Execute on_execute action event
    await OnExecuteAction.execute(controller, action, request_model)
    response: BaseResponse | Response = await action_method(**params_to_send)
    # Execute on_after action event
    await OnAfterAction.execute(controller, action, request_model, response)
    if issubclass(type(response), BaseResponse):
        ServiceProvider.reset_scoped(token)
        return response()

    ServiceProvider.reset_scoped(token)
    return response
