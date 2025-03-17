from typing import Any, Dict, List, Optional, Type, get_origin
import uuid

import yaml

from cafeto.responses import JSONResponse, PlainTextResponse, HTMLResponse, FileResponse
from cafeto.routing import Route
from cafeto.datastructures import UploadFile
from cafeto import responses as response_module
from cafeto.responses import formats
from cafeto.dependency_injection import ServiceCollection
from cafeto.websocket.websocket import WebSocket
from cafeto.models import BaseModel
from cafeto.schema import DefaultDocs
from cafeto.schema.library.schema import (
    ComponentSchema,
    Components,
    ExternalDocs,
    Info,
    Operation,
    Parameter,
    ParameterSchema,
    Parameters,
    Path,
    Paths,
    RequestBody,
    RequestBodyMediaType,
    RequestBodySchema,
    Response,
    ResponseContent,
    ResponseMediaType,
    ResponseSchema,
    Responses,
    Schema,
    Security,
    SecurityScheme,
    Tag,
    Tags
)
from cafeto.app import App
from cafeto.mvc.types import Action


def get_string_type(param_type: Type) -> str:
    """
    Returns the OpenAPI string representation of a given Python type.

    Args:
        param_type (Type): The Python type to be converted.

    Returns:
        str: The OpenAPI string representation of the given type.
             Returns 'string' for str, 'integer' for int, 'number' for float,
             and 'string' for any other type.
    """
    if param_type == str:
        return 'string'
    elif param_type == int:
        return 'number'
    elif param_type == float:
        return 'number'
    elif param_type == uuid.UUID:
        return 'string'
    else:
        return 'string'  # pragma: no cover


def get_string_format(param_type: Type) -> str:
    """
    Returns the OpenAPI string representation of a given Python type.

    Args:
        param_type (Type): The Python type to be converted.

    Returns:
        str: The OpenAPI string representation of the given type.
             Returns 'string' for str, 'integer' for int, 'number' for float,
             and 'string' for any other type.
    """
    if param_type == str:
        return 'string'
    elif param_type == int:
        return 'integer'
    elif param_type == float:
        return 'float'
    elif param_type == uuid.UUID:
        return 'uuid'
    else:
        return 'string'  # pragma: no cover


def get_route(routes: List[Route], url: str):
    """
    Retrieve a route from a list of routes that matches the given URL.

    Args:
        routes (List[Route]): A list of Route objects.
        url (str): The URL to match against the routes.

    Returns:
        Route: The route that matches the given URL, or None if no match is found.
    """
    for route in routes:
        if route.path == url:
            return route


def get_tag(action: Action) -> Tag:
    """
    Returns a Tag object for the given action.

    Args:
        action (Action): The action object containing the controller.

    Returns:
        Tag: A Tag object representing the controller.
    """
    controller = action.endpoint.controller
    docstring: Dict[str, Any] = {}
    if controller.__doc__ is not None:
        docstring = yaml.load(controller.__doc__, Loader=yaml.Loader)
    tag: Tag = Tag(controller.__name__, docstring.get('description', DefaultDocs.controller_description))

    return tag


def get_responses(action: Action, components: Components) -> Responses:
    """
    Returns a Responses object for the given action.

    Args:
        action (Action): The action object for which to generate the responses.
        components (Components): The Components object to store schemas.

    Returns:
        Responses: A Responses object containing the response objects for the action.
    """
    responses: Responses = Responses()

    if action.__doc__ is not None:
        docstring: Dict[str, Any] = yaml.load(action.__doc__, Loader=yaml.Loader)
        for key, value in docstring.get('responses', {}).items():
            status_code = key
            description = value.get('description', DefaultDocs.action_description_response)
            if value.get('default', False):
                response = get_response(action, status_code, description, components)
                responses.add_response(response)
            else:
                responses.add_response(
                    Response(status_code=status_code, content=ResponseContent(description=description))
                )

    else:
        description = DefaultDocs.action_description_response
        status_code = DefaultDocs.action_status_code
        response = get_response(action, status_code, description, components)
        responses.add_response(response)

    return responses


def get_response(action: Action, status_code: str, description: str, components: Components) -> Response:
    """
    Returns a Response object for the given action.

    Args:
        action (Action): The action object for which to generate the response.
        status_code (str): The HTTP status code for the response.
        description (str): The description of the response.
        components (Components): The Components object to store schemas.

    Returns:
        Response: A Response object containing the response object for the action.
    """
    response_object: Type = action.__annotations__.get('return', None)
    response_format: type[formats.FORMAT] = None
    if get_origin(response_object) is response_module.Format:
        response_format = response_object.__args__[1]
        response_object = response_object.__args__[0]

    if response_object is None:
        return Response(status_code=status_code, content=ResponseContent(description=description))

    if (
        response_object is list
        or response_object is tuple
        or get_origin(response_object) is list
        or get_origin(response_object) is tuple
    ):
        list_generic: BaseModel = response_object.__args__[0]
        media_type_schema = ResponseSchema(
            type='array',
            items=ResponseSchema(ref=f'#/components/schemas/{list_generic.__name__}')
        )
        response_media_type = ResponseMediaType(schema=media_type_schema)
        response_content = ResponseContent(description=description, content={'application/json': response_media_type})
        response = Response(status_code=status_code, content=response_content)

        component_schema = ComponentSchema(
            type='object',
            properties=list_generic.model_json_schema(ref_template='#/components/schemas/{model}')['properties']
        )
        components.schemas[list_generic.__name__] = component_schema

        return response

    elif (
        response_object is JSONResponse
        or response_object is dict
        or get_origin(response_object) is dict
    ):
        media_type_schema = ResponseSchema(type='object', additional_properties=True)
        response_media_type = ResponseMediaType(schema=media_type_schema)
        response_content = ResponseContent(description=description, content={'application/json': response_media_type})
        response = Response(status_code=status_code, content=response_content)
        return response

    elif response_object is FileResponse:  # pragma: no cover
        media_type_schema = ResponseSchema(type='string', format='binary')
        response_media_type = ResponseMediaType(schema=media_type_schema)
        response_content = ResponseContent(
            description=description,
            content={'application/octet-stream': response_media_type}
            )
        response = Response(status_code=status_code, content=response_content)
        return response

    elif response_object is str or response_object is PlainTextResponse:
        if response_format is None or response_format == formats.TEXT_PLAIN:
            media_type_schema = ResponseSchema(type='string')
            response_media_type = ResponseMediaType(schema=media_type_schema)
            response_content = ResponseContent(description=description, content={'text/plain': response_media_type})
        else:
            media_type_schema = ResponseSchema(type='string', format=response_format.value.split('/')[1])
            response_media_type = ResponseMediaType(schema=media_type_schema)
            response_content = ResponseContent(
                description=description,
                content={response_format.value: response_media_type}
                )
        response = Response(status_code=status_code, content=response_content)
        return response

    elif response_object is HTMLResponse:
        media_type_schema = ResponseSchema(type='string', format='html')
        response_media_type = ResponseMediaType(schema=media_type_schema)
        response_content = ResponseContent(description=description, content={'text/html': response_media_type})
        response = Response(status_code=status_code, content=response_content)
        return response

    else:
        media_type_schema = ResponseSchema(ref=f'#/components/schemas/{response_object.__name__}')
        response_media_type = ResponseMediaType(schema=media_type_schema)
        response_content = ResponseContent(description=description, content={'application/json': response_media_type})
        response = Response(status_code=status_code, content=response_content)

        component_schema = ComponentSchema(
            type='object',
            properties=response_object.model_json_schema(ref_template='#/components/schemas/{model}')['properties']
        )
        components.schemas[response_object.__name__] = component_schema

        return response


def get_request_body_info(
        action: Action,
        param_convertors: Dict[str, Type],
        components: Components
        ) -> RequestBody:
    """
    Returns a RequestBody object for the given action.

    Args:
        action (Action): The action object for which to generate the request body.
        param_convertors (Dict[str, Type]): A dictionary of parameter convertors.
        components (Components): The Components object to store schemas.

    Returns:
        RequestBody: A RequestBody object containing the request body object for the action.
    """
    request_object: Optional[Type[BaseModel]] = get_request_body_object(action, param_convertors)
    if request_object is None or request_object is WebSocket:
        return None

    if request_object is UploadFile:
        request_body_schema_properties = RequestBodySchema(type='string', format='binary')
        request_body_schema = RequestBodySchema(type='object', properties={'file': request_body_schema_properties})
        request_body_media_type = RequestBodyMediaType('multipart/form-data', schema=request_body_schema)
        request_body = RequestBody(request_body_media_type, description=None, required=True)

        return request_body
    else:
        request_body_schema = RequestBodySchema(ref=f'#/components/schemas/{request_object.__name__}')
        request_body_media_type = RequestBodyMediaType('application/json', schema=request_body_schema)
        request_body = RequestBody(request_body_media_type, description=None, required=True)

        model_schema = request_object.model_json_schema(ref_template='#/components/schemas/{model}')

        defs = model_schema.get('$defs', None)
        if defs:
            for key, value in defs.items():
                component_data_schema = ComponentSchema(type='object', properties=value['properties'])
                components.schemas[key] = component_data_schema

        component_data_schema = ComponentSchema(type='object', properties=model_schema['properties'])
        components.schemas[request_object.__name__] = component_data_schema

        return request_body


def get_request_body_object(
        action: Action,
        param_convertors: Dict[str, Type]
        ) -> Optional[Type[BaseModel]]:
    """
    Returns the request object for the given action.

    Args:
        action (Action): The action object for which to generate the request object.
        param_convertors (Dict[str, Type]): A dictionary of parameter convertors.

    Returns:
        Optional[Type[BaseModel]]: The request object for the action, or None if no request object is found.
    """
    annotations = action.__annotations__

    param_name: str
    param_type: Type
    for param_name, param_type in annotations.items():
        if param_name == 'return':
            continue  # pragma: no cover
        if (
            param_type in ServiceCollection.singleton
            or param_type in ServiceCollection.transient
            or param_type in ServiceCollection.scoped
        ):
            continue  # pragma: no cover
        if param_name in param_convertors:
            continue
        if param_name in action.endpoint.query:
            continue
        if param_name in action.endpoint.headers:
            continue

        return param_type


def get_security(action: Action, security_name: str) -> Optional[Security]:
    """
    Returns a Security object for the given action.

    Args:
        action (Action): The action object for which to generate the security object.
        security_name (str): The name of the security object.

    Returns:
        Optional[Security]: A Security object containing the security object for the action.
    """
    if hasattr(action, 'requires') and action.requires is not None:
        security = Security(security_name, action.requires.scope)
        return security


def get_parameters(action: Action, param_convertors: Dict[str, Type]) -> Optional[Parameters]:
    """
    Returns a Parameters object for the given action.

    Args:
        action (Action): The action object for which to generate the parameters.
        param_convertors (Dict[str, Type]): A dictionary of parameter convertors.

    Returns:
        Optional[Parameters]: A Parameters object containing the parameters for the action.
    """
    params: Parameters = Parameters()
    annotations: Dict[str, Type] = action.__annotations__

    default_values = action.endpoint.default_values

    param_name: str
    param_type: Type
    for param_name, param_type in annotations.items():
        if param_name in param_convertors:
            parameter_schema = ParameterSchema(type=get_string_type(param_type), format=get_string_format(param_type))

            params.add_parameter(Parameter(
                name=param_name,
                in_='path',
                required=True,
                schema=parameter_schema
            ))
        if param_name in action.endpoint.query:
            parameter_schema = ParameterSchema(type=get_string_type(param_type), format=get_string_format(param_type))

            default_value = default_values.get(param_name, None)

            params.add_parameter(Parameter(
                name=param_name,
                in_='query',
                required=default_value is None,
                schema=parameter_schema,
                default=default_value
            ))
        if param_name in action.endpoint.headers:
            parameter_schema = ParameterSchema(type=get_string_type(param_type), format=get_string_format(param_type))

            default_value = default_values.get(param_name, None)

            params.add_parameter(Parameter(
                name=param_name,
                in_='header',
                required=default_value is None,
                schema=parameter_schema,
                default=default_value
            ))

    if len(params.parameters) == 0:
        return None
    return params


def get_operation(
        action: Action,
        responses: Responses,
        request_body: Optional[RequestBody],
        security: Optional[Security],
        parameters: Optional[Parameters]
        ) -> Operation:
    """
    Returns an Operation object for the given action.

    Args:
        action (Action): The action object for which to generate the operation.
        responses (Responses): The responses object for the action.
        request (Optional[RequestBody]): The request object for the action.
        security (Optional[Security]): The security object for the action.
        parameters (Optional[Parameters]): The parameters object for the action.

    Returns:
        Operation: An Operation object containing the operation for the action.
    """
    summary = DefaultDocs.action_summary
    description = DefaultDocs.action_description
    if action.__doc__ is not None:
        docstring: Dict[str, str] = yaml.load(action.__doc__, Loader=yaml.Loader)
        summary = docstring.get('summary', DefaultDocs.action_summary)
        description = docstring.get('description', DefaultDocs.action_description)

    operation: Operation = Operation(
        tags=[action.endpoint.controller.__name__],
        summary=summary,
        operation_id=action.endpoint.controller.__name__.lower() + '__' + action.__name__.lower(),
        description=description,
        responses=responses,
        request_body=request_body,
        security=security,
        parameters=parameters)
    return operation


def get_path(action: Action, operation: Operation) -> Optional[Path]:
    """
    Returns a Path object for the given action.

    Args:
        action (Action): The action object for which to generate the path.
        operation (Operation): The operation object for the action.

    Returns:
        Optional[Path]: A Path object containing the path for the action.
    """
    if action.endpoint.method == 'WEBSOCKET':
        return  # pragma: no cover
    return Path(**{action.endpoint.method.lower(): operation})


def create_schema(
        app: App,
        openapi_version: str = '3.0.1',
        info: Optional[Info] = None,
        security_schema: Optional[SecurityScheme] = None,
        external_docs: Optional[ExternalDocs] = None
        ) -> Schema:
    """
    Creates an OpenAPI schema for the given app.

    Args:
        app (App): The app for which to generate the schema.
        openapi_version (str): The version of the OpenAPI specification. Defaults to '3.0.1'.
        info (Optional[Info]): The info object for the schema. Defaults to None.
        security_schema (Optional[SecurityScheme]): The security scheme object for the schema. Defaults to None.
        external_docs (Optional[ExternalDocs]): The external docs object for the schema. Defaults to None.

    Returns:
        Schema: An OpenAPI schema for the given app.
    """

    tags: Tags = Tags()
    components: Components = Components()
    paths: Paths = Paths()

    for action in app.action_list:
        tag: Tag = get_tag(action)
        tags.add_tag(tag)
        responses: Responses = get_responses(action, components)
        request_info: Optional[RequestBody] = get_request_body_info(
            action,
            get_route(app.routes, action.endpoint.path).param_convertors, components
        )
        security_schema_name = security_schema.name if security_schema is not None else 'auth002'
        security_requirement: Optional[Security] = get_security(action, security_schema_name)
        parameters: Optional[Parameters] = get_parameters(
            action,
            get_route(app.routes, action.endpoint.path).param_convertors
        )

        operation: Operation = get_operation(action, responses, request_info, security_requirement, parameters)
        path: Optional[Path] = get_path(action, operation)
        if path is not None:
            paths.add_path(action.endpoint.path, path)

    if info is None:
        info = Info(title=DefaultDocs.title, version=DefaultDocs.version)

    if security_schema is not None:
        components.security_schemes = security_schema

    schema: Schema = Schema(
        openapi_version=openapi_version,
        info=info,
        external_docs=external_docs,
        tags=tags,
        paths=paths,
        components=components
    )

    return schema.to_dict()
