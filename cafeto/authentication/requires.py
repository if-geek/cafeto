from typing import Sequence


class Requires:
    """
    A class to enforce scope-based access control on endpoints.
    Attributes:
        scope (str | Sequence[str]): The required scope(s) for the endpoint.
        status_code (int): The HTTP status code to return if access is denied. Defaults to 403.
        redirect (str | None): The URL to redirect to if access is denied. Defaults to None.
    """
    def __init__(self, scope: str | Sequence[str], status_code: int = 403, redirect: str | None = None):
        self.scope = scope if isinstance(scope, Sequence) else [scope]
        self.status_code = status_code
        self.redirect = redirect
