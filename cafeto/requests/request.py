from typing import Any, Dict, Type
from starlette.requests import Request as StarletteRequest

from cafeto.errors.errors import ModelError, RequestError, format_errors
from cafeto.models.base_model import BaseModel


class Request(StarletteRequest):
    """
    A custom Request class that extends Starlette's Request class.
    Args:
        request (StarletteRequest): An instance of Starlette's Request class.
    Inherits:
        StarletteRequest: The base class for handling HTTP requests in Starlette.
    """

    def __init__(self, request: StarletteRequest):
        super().__init__(request.scope, request._receive, request._send)


async def get_request_body_model(
        data: Dict[str, Any],
        param_type: Type[BaseModel],
        body: Dict[str, Any] = {}
        ) -> BaseModel:
    """
    Asynchronously creates and validates a request body model.

    Args:
        data (Dict[str, Any]): The data to be used for creating the model.
        param_type (Type[BaseModel]): The type of the model to be created.
        body (Dict[str, Any], optional): Additional parameters for validation. Defaults to {}.

    Returns:
        BaseModel: The created and validated model.

    Raises:
        RequestError: If there is an error during model creation or validation.
    """
    try:
        model = param_type.create(data)
        if 'validator' in body:
            if body['validator'] is not None:
                await model.check(body['validator'])
        else:
            await model.check()
        return model
    except ModelError as e:
        raise RequestError(format_errors(e.errors))
