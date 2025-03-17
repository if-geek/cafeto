from types import GeneratorType, AsyncGeneratorType
from typing import Generic, Optional, Type, TypeVar

from cafeto.models import BaseModel
from cafeto.background import BackgroundTask
from cafeto import responses

from cafeto.responses.codes import (
    STATUS_CODE, CODE_200_OK, CODE_201_CREATED, CODE_204_NO_CONTENT,
    CODE_400_BAD_REQUEST, CODE_401_UNAUTHORIZED, CODE_403_FORBIDDEN, CODE_404_NOT_FOUND,
    CODE_405_METHOD_NOT_ALLOWED, CODE_409_CONFLICT, CODE_500_INTERNAL_SERVER_ERROR,
    CODE_501_NOT_IMPLEMENTED, CODE_503_SERVICE_UNAVAILABLE, CODE_504_GATEWAY_TIMEOUT
)

from cafeto.responses.formats import (
    FORMAT, APPLICATION_JSON, TEXT_PLAIN, TEXT_HTML
)

from cafeto.mvc.types import ResponseBody

TFormat = TypeVar('TFormat', bound=Type)


class Format(Generic[ResponseBody, TFormat]):
    """
    A generic class that represents a format for a response.

    This class uses two generic type parameters:
    - ResponseBody: The type of the response.
    - TFormat: The type of the format.

    Examples:
        Format[str, TEXT_PLAIN]: A format for a plain text response.
    """
    pass


class BaseResponse(Generic[ResponseBody]):
    """
    A base class for handling different types of responses in an application.
    Attributes:
        response_body (ResponseBody): The response response_body.
        format (Type[FORMAT]): The format of the response, default is APPLICATION_JSON.
        status_code (Type[STATUS_CODE]): The HTTP status code of the response, default is CODE_200_OK.
        background (Optional[BackgroundTask]): Optional background task to be executed.
    Methods:
        __call__(mode: str = 'http'):
            Calls the appropriate response method based on the mode ('http' or 'ws').
        response_http():
            Handles HTTP responses based on the type of response_body provided.
        response_ws():
            Handles WebSocket responses.
    """
    def __init__(
            self,
            response_body: ResponseBody,
            format: Type[FORMAT] = APPLICATION_JSON,
            status_code: Type[STATUS_CODE] = CODE_200_OK,
            background: Optional[BackgroundTask] = None
            ):
        self.response_body: ResponseBody = response_body
        self.format: Type[FORMAT] = format
        self.status_code: Type[STATUS_CODE] = status_code
        self.background: Optional[BackgroundTask] = background

    def __call__(self, mode: str = 'http'):
        if mode == 'http':
            return self.response_http()
        return self.response_ws()

    def response_http(self):
        if isinstance(self.response_body, dict):
            return responses.JSONResponse(
                self.response_body,
                status_code=self.status_code.value,
                background=self.background
                )
        if isinstance(self.response_body, list):
            if any(issubclass(type(item), BaseModel) for item in self.response_body):
                return responses.ModelResponse(
                    self.response_body,
                    status_code=self.status_code.value,
                    background=self.background
                    )
            else:
                return responses.JSONResponse(
                    self.response_body,
                    status_code=self.status_code.value,
                    background=self.background
                    )
        if isinstance(self.response_body, BaseModel):
            return responses.ModelResponse(
                self.response_body,
                status_code=self.status_code.value,
                background=self.background
                )
        if (
            isinstance(self.response_body, AsyncGeneratorType)
            or isinstance(self.response_body, GeneratorType)
        ):  # pragma: no cover
            return responses.StreamingResponse(
                self.response_body,
                status_code=self.status_code.value,
                media_type=self.format.value,
                background=self.background
                )
        if self.format == TEXT_HTML:
            return responses.HTMLResponse(
                self.response_body,
                status_code=self.status_code.value,
                background=self.background
                )
        if self.format == TEXT_PLAIN or isinstance(self.response_body, str):
            return responses.PlainTextResponse(
                self.response_body,
                status_code=self.status_code.value,
                background=self.background
                )
        if isinstance(self.response_body, responses.FileResponse):  # pragma: no cover
            return self.response_body
        if self.response_body is None:
            return responses.Response(status_code=self.status_code.value, background=self.background)

    def response_ws(self):
        return responses.ModelWSResponse(
            self.response_body,
            status_code=self.status_code.value,
            background=self.background
            )


class Ok(BaseResponse):  # pragma: no cover
    class Ok(BaseResponse):
        """
        A response class representing a successful HTTP 200 OK response.

        Attributes:
            response_body (ResponseBody): The response response_body.
            format (Type): The format of the response, default is APPLICATION_JSON.
            background (Optional[BackgroundTask]): An optional background task to be executed.

        Methods:
            __init__(response_body: ResponseBody, format: Type = APPLICATION_JSON,
                background: Optional[BackgroundTask] = None):
                Initializes the Ok response with the given response_body, format, and optional background task.
        """
    def __init__(
            self,
            response_body: ResponseBody,
            format: Type = APPLICATION_JSON,
            background: Optional[BackgroundTask] = None
            ):
        super().__init__(response_body, format, CODE_200_OK, background)


class Created(BaseResponse):  # pragma: no cover
    """
    A response class representing a successful HTTP 201 Created response.

    Attributes:
        response_body (ResponseBody): The response response_body.
        format (Type): The format of the response, default is APPLICATION_JSON.

    Methods:
        __init__(response_body: ResponseBody, format: Type = APPLICATION_JSON):
            Initializes the Created response with the given response_body and format.`
    """
    def __init__(self, response_body: ResponseBody, format: Type = APPLICATION_JSON):
        super().__init__(response_body, format, CODE_201_CREATED)


class NoContent(BaseResponse):  # pragma: no cover
    """
    A response class representing a successful HTTP 204 No Content response.

    Attributes:
        background (Optional[BackgroundTask]): An optional background task to be executed

    Methods:
        __init__(background: Optional[BackgroundTask] = None):
            Initializes the NoContent response with the given background task.
    """
    def __init__(
            self,
            background: Optional[BackgroundTask] = None
            ):
        super().__init__(None, TEXT_PLAIN, CODE_204_NO_CONTENT, background=background)


class BadRequest(BaseResponse):  # pragma: no cover
    """
    A response class representing an HTTP 400 Bad Request response.

    Attributes:
        response_body (ResponseBody): The response response_body.
        format (Type): The format of the response, default is APPLICATION_JSON.

    Methods:
        __init__(response_body: ResponseBody, format: Type = APPLICATION_JSON,
            background: Optional[BackgroundTask] = None):
            Initializes the BadRequest response with the given response_body, format, and optional background task.
    """
    def __init__(
            self,
            response_body: ResponseBody,
            format: Type = APPLICATION_JSON,
            background: Optional[BackgroundTask] = None
            ):
        super().__init__(response_body, format, CODE_400_BAD_REQUEST, background)


class Unauthorized(BaseResponse):  # pragma: no cover
    """
    A response class representing an HTTP 401 Unauthorized response.

    Attributes:
        response_body (ResponseBody): The response response_body.
        format (Type): The format of the response, default is APPLICATION_JSON.

    Methods:
        __init__(response_body: ResponseBody, format: Type = APPLICATION_JSON,
            background: Optional[BackgroundTask] = None):
            Initializes the Unauthorized response with the given response_body, format, and optional background task.
    """
    def __init__(
            self,
            response_body: ResponseBody,
            format: Type = APPLICATION_JSON,
            background: Optional[BackgroundTask] = None
            ):
        super().__init__(response_body, format, CODE_401_UNAUTHORIZED, background)


class Forbidden(BaseResponse):  # pragma: no cover
    """
    A response class representing an HTTP 403 Forbidden response.

    Attributes:
        response_body (ResponseBody): The response response_body.
        format (Type): The format of the response, default is APPLICATION_JSON.

    Methods:
        __init__(response_body: ResponseBody, format: Type = APPLICATION_JSON,
            background: Optional[BackgroundTask] = None):
            Initializes the Forbidden response with the given response_body, format, and optional background task.
    """
    def __init__(
            self,
            response_body: ResponseBody,
            format: Type = APPLICATION_JSON,
            background: Optional[BackgroundTask] = None
            ):
        super().__init__(response_body, format, CODE_403_FORBIDDEN, background)


class NotFound(BaseResponse):  # pragma: no cover
    """
    A response class representing an HTTP 404 Not Found response.

    Attributes:
        response_body (ResponseBody): The response response_body.
        format (Type): The format of the response, default is APPLICATION_JSON.

    Methods:
        __init__(response_body: ResponseBody, format: Type = APPLICATION_JSON,
            background: Optional[BackgroundTask] = None):
            Initializes the NotFound response with the given response_body, format, and optional background task.
    """
    def __init__(
            self,
            response_body: ResponseBody,
            format: Type = APPLICATION_JSON,
            background: Optional[BackgroundTask] = None
            ):
        super().__init__(response_body, format, CODE_404_NOT_FOUND, background)


class MethodNotAllowed(BaseResponse):  # pragma: no cover
    """
    A response class representing an HTTP 405 Method Not Allowed response.

    Attributes:
        response_body (ResponseBody): The response response_body.
        format (Type): The format of the response, default is APPLICATION_JSON.

    Methods:
        __init__(response_body: ResponseBody, format: Type = APPLICATION_JSON,
            background: Optional[BackgroundTask] = None):
            Initializes the MethodNotAllowed response with the given response_body, format, and optional
            background task.
    """
    def __init__(
            self,
            response_body: ResponseBody,
            format: Type = APPLICATION_JSON,
            background: Optional[BackgroundTask] = None
            ):
        super().__init__(response_body, format, CODE_405_METHOD_NOT_ALLOWED, background)


class Conflict(BaseResponse):  # pragma: no cover
    """
    A response class representing an HTTP 409 Conflict response.

    Attributes:
        response_body (ResponseBody): The response response_body.
        format (Type): The format of the response, default is APPLICATION_JSON.

    Methods:
        __init__(response_body: ResponseBody, format: Type = APPLICATION_JSON,
            background: Optional[BackgroundTask] = None):
            Initializes the Conflict response with the given response_body, format, and optional background task.
    """
    def __init__(
            self,
            response_body: ResponseBody,
            format: Type = APPLICATION_JSON,
            background: Optional[BackgroundTask] = None
            ):
        super().__init__(response_body, format, CODE_409_CONFLICT, background)


class InternalServerError(BaseResponse):  # pragma: no cover
    """
    A response class representing an HTTP 500 Internal Server Error response.

    Attributes:
        response_body (ResponseBody): The response response_body.
        format (Type): The format of the response, default is APPLICATION_JSON.

    Methods:
        __init__(response_body: ResponseBody, format: Type = APPLICATION_JSON,
            background: Optional[BackgroundTask] = None):
            Initializes the InternalServerError response with the given response_body, format, and optional
            background task.
    """
    def __init__(
            self,
            response_body: ResponseBody,
            format: Type = APPLICATION_JSON,
            background: Optional[BackgroundTask] = None
            ):
        super().__init__(response_body, format, CODE_500_INTERNAL_SERVER_ERROR, background)


class NotImplemented(BaseResponse):  # pragma: no cover
    """
    A response class representing an HTTP 501 Not Implemented response.

    Attributes:
        response_body (ResponseBody): The response response_body.
        format (Type): The format of the response, default is APPLICATION_JSON.

    Methods:
        __init__(response_body: ResponseBody, format: Type = APPLICATION_JSON,
            background: Optional[BackgroundTask] = None):
            Initializes the NotImplemented response with the given response_body, format, and optional background task.
    """
    def __init__(
            self,
            response_body: ResponseBody,
            format: Type = APPLICATION_JSON,
            background: Optional[BackgroundTask] = None
            ):
        super().__init__(response_body, format, CODE_501_NOT_IMPLEMENTED, background)


class ServiceUnavailable(BaseResponse):  # pragma: no cover
    """
    A response class representing an HTTP 503 Service Unavailable response.

    Attributes:
        response_body (ResponseBody): The response response_body.
        format (Type): The format of the response, default is APPLICATION_JSON.

    Methods:
        __init__(response_body: ResponseBody, format: Type = APPLICATION_JSON,
            background: Optional[BackgroundTask] = None):
            Initializes the ServiceUnavailable response with the given response_body, format, and optional
            background task.
    """
    def __init__(
            self,
            response_body: ResponseBody,
            format: Type = APPLICATION_JSON,
            background: Optional[BackgroundTask] = None
            ):
        super().__init__(response_body, format, CODE_503_SERVICE_UNAVAILABLE, background)


class GatewayTimeout(BaseResponse):  # pragma: no cover
    """
    A response class representing an HTTP 504 Gateway Timeout response.

    Attributes:
        response_body (ResponseBody): The response response_body.
        format (Type): The format of the response, default is APPLICATION_JSON.

    Methods:
        __init__(response_body: ResponseBody, format: Type = APPLICATION_JSON,
            background: Optional[BackgroundTask] = None):
            Initializes the GatewayTimeout response with the given response_body, format, and optional background task.
    """
    def __init__(
            self,
            response_body: ResponseBody,
            format: Type = APPLICATION_JSON,
            background: Optional[BackgroundTask] = None
            ):
        super().__init__(response_body, format, CODE_504_GATEWAY_TIMEOUT, background)
