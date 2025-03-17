from abc import ABC
from typing import Any, Dict, Generic

from cafeto.mvc.types import RequestModel


class AContextService(ABC):
    """
    AContextService is an abstract base class that defines the structure for a context service.

    Attributes:
        path (str): The path of the request.
        method (str): The HTTP method of the request.
        headers (Dict[str, Any]): The headers of the request.
        query (Dict[str, Any]): The query parameters of the request.
        controller_name (str): The name of the controller handling the request.
        action_name (str): The name of the action being performed.
        request_model (RequestModel): The model representing the request data.
    """
    path: str
    method: str
    headers: Dict[str, Any]
    query: Dict[str, Any]
    controller_name: str
    action_name: str
    request_model: RequestModel

    def set_data(
            self,
            path: str,
            method: str,
            headers: Dict[str, Any],
            query: Dict[str, Any],
            controller_name: str,
            action_name: str,
            request_model: RequestModel
            ): ...

    def to_json(self): ...


class ContextService(Generic[RequestModel], AContextService):
    """
    A service class that handles the context of a request, including path, method, headers, query parameters,
    controller name, action name, and the request model.

    Attributes:
        path (str): The path of the request.
        method (str): The HTTP method of the request.
        headers (Dict[str, Any]): The headers of the request.
        query (Dict[str, Any]): The query parameters of the request.
        controller_name (str): The name of the controller that will handle the request.
        action_name (str): The name of the action that will handle the request.
        request_model (RequestModel): The request model of the request.
    """

    def set_data(
            self,
            path: str,
            method: str,
            headers: Dict[str, Any],
            query: Dict[str, Any],
            controller_name: str,
            action_name: str,
            request_model: RequestModel
            ):
        """
        Sets the context data for a request.

        Args:
            path (str): The path of the request.
            method (str): The HTTP method of the request.
            headers (Dict[str, Any]): The headers of the request.
            query (Dict[str, Any]): The query parameters of the request.
            controller_name (str): The name of the controller handling the request.
            action_name (str): The name of the action being performed.
            request_model (RequestModel): The model representing the request data.
        """
        self.path: str = path
        self.method: str = method
        self.headers: Dict[str, Any] = headers
        self.query: Dict[str, Any] = query
        self.controller_name: str = controller_name
        self.action_name: str = action_name
        self.request_model: RequestModel = request_model

    def to_json(self):
        """
        Converts the context service data to a JSON-serializable dictionary.

        Returns:
            dict: A dictionary containing the context service data with the following keys:
                - 'path' (str): The request path.
                - 'method' (str): The HTTP method of the request.
                - 'headers' (dict): The request headers.
                - 'query' (dict): The query parameters of the request.
                - 'controller_name' (str): The name of the controller handling the request.
                - 'action_name' (str): The name of the action being executed.
                - 'request_model' (dict): The JSON-serializable representation of the request model.
        """
        request_model_json = self.request_model.model_dump(mode='json')
        return {
            'path': self.path,
            'method': self.method,
            'headers': self.headers,
            'query': self.query,
            'controller_name': self.controller_name,
            'action_name': self.action_name,
            'request_model': request_model_json
        }
