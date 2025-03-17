from typing import Any, Dict, Optional, Sequence


class Endpoint:
    """
    Represents an API endpoint with its associated path, method, query parameters, headers, and default values.

    Attributes:
        path (str): The URL path of the endpoint.
        method (str): The HTTP method (e.g., 'GET', 'POST') used by the endpoint.
        query (Optional[Sequence[str]]): A list of query parameter names expected by the endpoint. Defaults to
        an empty list.
        headers (Optional[Sequence[str]]): A list of header names expected by the endpoint. Defaults to an empty list.
        default_values (dict): A dictionary of default values for the endpoint's parameters. Defaults to an
        empty dictionary.
        controller (type[BaseController]): The controller class associated with the endpoint. Defaults to None.
    """
    def __init__(
            self,
            path: str,
            method: str,
            query: Optional[Sequence[str]] = [],
            headers: Optional[Sequence[str]] = [],
            body: Optional[Dict[str, Any]] = {},
            default_values: Optional[dict] = {}
            ):
        from cafeto.mvc.base_controller import BaseController

        self.path = path
        self.method = method
        self.query = query
        self.headers = headers
        self.body = body
        self.default_values = default_values
        self.controller: type[BaseController] = None
