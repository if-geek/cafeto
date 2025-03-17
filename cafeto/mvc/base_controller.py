from cafeto.websocket.websocket import WebSocket
from cafeto.requests.request import Request


class BaseController(object):
    """
    BaseController is a base class for handling requests.

    Attributes:
        request (Request): An instance of the Request class representing the incoming request.
    """

    request: Request
    websocket: WebSocket
