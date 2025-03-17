import json
from typing import Any, Awaitable, Callable, Dict

from starlette.websockets import WebSocket as StarletteWebSocket

from cafeto.requests.request import get_request_body_model
from cafeto.responses import BaseResponse
from cafeto.responses.model_response import ModelWSResponse
from cafeto.models.base_model import BaseModel
from cafeto.errors.errors import RequestError

from cafeto.mvc.types import ResponseBody


class WebSocket(StarletteWebSocket):
    """
    A class to handle WebSocket connections using Starlette.

    Attributes:
        on_receive (Callable[[BaseModel], Awaitable[ResponseBody]]): Callback for handling received messages.
        on_connect (Callable[[], Awaitable]): Callback for handling connection establishment.
        on_disconnect (Callable[[], Awaitable]): Callback for handling connection termination.
        param_type: The type of the parameter expected by the on_receive callback.
    """

    def __init__(self, websocket: StarletteWebSocket):
        super().__init__(websocket.scope, websocket._receive, websocket._send)
        self.on_receive: Callable[[BaseModel], Awaitable[ResponseBody]] = None
        self.on_connect: Callable[[], Awaitable] = None
        self.on_disconnect: Callable[[], Awaitable] = None
        self.param_type: BaseModel = None
        self.in_loop: bool = True
        self.body: Dict[str, Any] = None

    async def accept_callback(
            self,
            on_receive: Callable[[BaseModel], Awaitable] = None,
            on_connect: Callable[[], Awaitable] = None,
            on_disconnect: Callable[[], Awaitable] = None
            ) -> None:
        """
        Handles the acceptance of a WebSocket connection and manages the lifecycle events.

        Args:
            on_receive (Callable[[BaseModel], Awaitable], optional): A callback function to handle received messages.
            on_connect (Callable[[], Awaitable], optional): A callback function to handle the connection event.
            on_disconnect (Callable[[], Awaitable], optional): A callback function to handle the disconnection event.

        Raises:
            RequestError: If there is an error in the request_body.
            Exception: For any other exceptions that occur during the WebSocket communication.
        """

        self.on_connect = on_connect
        self.on_disconnect = on_disconnect
        self.on_receive = on_receive

        await self.accept()
        await self.__on_connect()

        try:
            while self.in_loop:
                data = await self.receive_json()
                response: ModelWSResponse[ResponseBody] = await self.__on_receive(data)
                await response(send=self.send_bytes)
        except RequestError as e:
            data = {
                "statusCode": 400,
                "body": e.errors
            }
            await self.send_bytes(json.dumps(data).encode('utf-8'))
        except Exception:
            self.in_loop = False
        finally:
            await self.__on_disconnect()

    async def __on_connect(self):
        """
        Asynchronous method that is called when a connection is established.

        If the `on_connect` callback is defined, it will be awaited and executed.
        """
        if self.on_connect is not None:
            await self.on_connect()

    async def __on_disconnect(self):
        """
        Asynchronous method that handles the disconnection event.

        This method is called when a disconnection occurs. If a callback function
        for the disconnection event (`on_disconnect`) is defined, it will be awaited
        and executed.
        """
        if self.on_disconnect is not None:
            await self.on_disconnect()

    async def close(self):
        """
        Asynchronously closes the WebSocket connection and sets the in_loop flag to False.

        This method overrides the close method from the superclass to perform additional
        cleanup specific to this class.
        """
        await super().close()
        self.in_loop = False

    async def __on_receive(self, data: Dict[str, Any]) -> ModelWSResponse[ResponseBody]:
        """
        Handles the reception of data over a WebSocket connection.
        This method is called when data is received. It processes the data,
        converts it into a request model, and then calls the `on_receive` method
        with the request model. The response from `on_receive` is then returned.

        Args:
            data (Dict[str, Any]): The data received over the WebSocket connection.

        Returns:
            ModelWSResponse[ResponseBody]: The response to be sent back over the WebSocket connection.
        """
        if self.param_type is None:
            annotations = self.on_receive.__annotations__
            self.param_type = list(annotations.values())[0]

        request_model: BaseModel = await get_request_body_model(data, self.param_type, self.body)
        response: ModelWSResponse | BaseResponse = await self.on_receive(request_model)

        if issubclass(type(response), BaseResponse):
            return response(mode='ws')

        return response
