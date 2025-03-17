from __future__ import annotations

import json
from typing import Mapping, Generic, Optional

from starlette.responses import Response

from pydantic.main import IncEx

from cafeto.background import BackgroundTask
from cafeto.models.base_model import BaseModel
from cafeto.types import SendWs
from cafeto.mvc.types import ResponseBody


class ModelResponse(Response, Generic[ResponseBody]):
    """
    A custom response class that extends the base Response class to handle
    responses with a specific response_body model.

    Attributes:
        response_body (ResponseBody): The response_body of the response, expected to be a model instance.
        status_code (int): The HTTP status code of the response. Defaults to 200.
        headers (Mapping[str, str] | None): Optional headers to include in the response.
        media_type (str | None): The media type of the response. Defaults to 'application/json'.
        background (BackgroundTask | None): Optional background task to run after the response is sent.
    """
    def __init__(
        self,
        response_body: ResponseBody,
        status_code: int = 200,
        headers: Mapping[str, str] | None = None,
        media_type: str | None = 'application/json',
        background: BackgroundTask | None = None,
        include: IncEx | None = None,
        exclude: IncEx | None = None,
    ) -> None:
        self.include = include
        self.exclude = exclude
        super().__init__(response_body, status_code, headers, media_type, background)

    def render(self, response_body: ResponseBody) -> bytes:
        """
        Renders the response body as a JSON-encoded byte string.

        Args:
            response_body (ResponseBody): The response body to render. It can be either a single instance or a
            list of instances.

        Returns:
            bytes: The JSON-encoded byte string representation of the response body.
        """
        if isinstance(response_body, list):
            return BaseModel.model_dump_json_many(
                response_body,
                include=self.include,
                exclude=self.exclude
                ).encode('utf-8')
        return response_body.model_dump_json(include=self.include, exclude=self.exclude).encode('utf-8')


class ModelWSResponse(Generic[ResponseBody]):
    """
    A WebSocket response model that handles the serialization and sending of response body,
    emulating an HTTP response with a status code and body.

    Attributes:
        response_body (ResponseBody | List[ResponseBody]): The response response_body, which can be a single instance
        or a list of instances.
        status_code (int): The HTTP status code for the response. Defaults to 200.
        background (BackgroundTask | None): An optional background task to be executed after sending the response.
        include (IncEx | None): Fields to include in the serialized response.
        exclude (IncEx | None): Fields to exclude from the serialized response.
        body (str): The serialized response response_body.
    """
    def __init__(
            self,
            response_body: ResponseBody,
            status_code: int = 200,
            background: BackgroundTask | None = None,
            include: Optional[IncEx] = None,
            exclude: Optional[IncEx] = None
    ) -> None:
        self.response_body = response_body
        self.status_code = status_code
        self.background = background
        self.include = include
        self.exclude = exclude
        self.body = self.render(response_body)

    def render(self, response_body: ResponseBody) -> str:
        """
        Renders the response body into a JSON string.

        Args:
            response_body (ResponseBody): The response body to render. It can be a list of BaseModel instances,
                a single BaseModel instance, or any other type.

        Returns:
            str: The JSON string representation of the response body. If the response body is a list of BaseModel
                 instances, it returns a JSON array. If it is a single BaseModel instance, it returns a JSON object.
                 If the response body is None or an empty string, it returns 'null'. Otherwise, it returns the JSON
                 string of the response body.
        """
        if isinstance(response_body, list):
            if any(isinstance(item, BaseModel) for item in response_body):
                return BaseModel.model_dump_json_many(response_body, include=self.include, exclude=self.exclude)

        if isinstance(response_body, BaseModel):
            return response_body.model_dump_json(include=self.include, exclude=self.exclude)

        if response_body is None or response_body == '':
            return 'null'

        return json.dumps(response_body)

    async def __call__(self, send: SendWs):
        """
        Asynchronously sends a WebSocket response with the status code and body.

        Args:
            send (SendWs): A callable that sends the WebSocket message.

        Returns:
            None

        Sends a JSON formatted response containing the status code and body.
        If a background task is provided, it will be awaited after sending the response.
        """
        await send(f"""
{{
    "statusCode": {self.status_code},
    "body": {self.body}
}}
""".encode('utf-8')
            )
        if self.background is not None:
            await self.background()
