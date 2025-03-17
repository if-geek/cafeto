from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, Union, overload

from pydantic_core import ErrorDetails

if TYPE_CHECKING:  # pragma: no cover
    from cafeto.app import CafetoConfig


class ParamConvertError(Exception):  # pragma: no cover
    """
    Exception raised when a parameter cannot be converted to the specified type.

    Attributes:
        param (str): The parameter that failed to convert.
        type (Type): The type to which the parameter was supposed to be converted.
    """

    def __init__(self, param: str, type: Type) -> None:
        self.param = param
        self.type = type

    def __str__(self) -> str:
        return f"Cannot convert {self.param} to {self.type}"


class Error:
    """
    A class to create error details for validation errors.
    """

    @overload
    def __new__(cls, type: str, msg: str) -> ErrorDetails:
        ...  # pragma: no cover

    def __new__(cls, type: str, msg: str, loc: Optional[List[str] | str] = None) -> ErrorDetails:
        """
        Creates a new ErrorDetails instance.

        Args:
            type (str): The type of the error.
            msg (str): The error message.
            loc (Optional[List[str] | str]): The location of the error, if any.

        Returns:
            ErrorDetails: The created error details.
        """

        return_value = {
            'type': type,
            'msg': msg,
        }
        if loc is not None:
            if isinstance(loc, str):
                return_value['loc'] = [loc]
            else:
                return_value['loc'] = loc

        return return_value


class FieldError(Exception):
    """
    Exception raised for errors related to a specific field.

    Attributes:
        error (Error): The error details for the field.
    """

    def __init__(self, error: Error) -> None:
        self.error: Error = error


class ModelError(Exception):
    """
    Exception raised for errors related to a model.

    Attributes:
        errors (List[Error]): A list of error details for the model.
    """

    def __init__(self, errors: List[Error]) -> None:
        self.errors: List[Error] = errors


class RequestError(Exception):
    """
    Exception raised for errors related to a response.

    Attributes:
        error (Error): The error details for the response.
    """

    def __init__(self, errors: Dict[str, Any]) -> None:
        self.errors: Dict[str, Any] = errors


def format_errors(errors: List[Error], config: Optional['CafetoConfig'] = None) -> Dict[str, Any]:
    """
    Formats a list of errors into a dictionary based on the provided configuration.

    Args:
        errors (List[Error]): A list of Error objects to be formatted.
        config (Optional['CafetoConfig']): An optional configuration object. If not provided,
            the configuration from the App instance will be used.

    Returns:
        Dict[str, Any]: A dictionary containing the formatted errors. The key for the error list
            is determined by the configuration. If the configuration specifies an error object, it will be included
            in the dictionary as well.
    """
    from cafeto.app import App

    if config is None:
        config = App.instance.config
    error_list_key: str = config.error_list_key
    error_response = {
        error_list_key: errors
    }
    if config.error_object:
        error_response[config.error_object_key] = create_recursive_dict(errors)

    return error_response


def create_recursive_dict(errors: List[Error]) -> Dict[str, Any]:
    """
    Creates a nested dictionary from a list of errors, where each error is added to the dictionary
    based on its location.

    Args:
        errors (List[Error]): A list of error dictionaries. Each error dictionary must contain
            'loc' (a list of strings or integers indicating the location of the error),
            'type' (a string indicating the type of error), and 'msg' (a string
            containing the error message).

    Returns:
        Dict[str, Any]: A nested dictionary where the keys are the elements of the 'loc' lists from
            the errors, and the values are lists of error dictionaries containing 'type'
            and 'msg' for each error at that location.
    """

    def add_error_to_dict(d: Dict[str, Any], loc: List[Union[str, int]], error: Dict[str, Any]):
        if len(loc) == 1:
            if loc[0] not in d or not isinstance(d[loc[0]], list):
                d[loc[0]] = []
            d[loc[0]].append({'type': error['type'], 'msg': error['msg']})
        else:
            if loc[0] not in d or not isinstance(d[loc[0]], dict):
                d[loc[0]] = {}
            add_error_to_dict(d[loc[0]], loc[1:], error)

    error_dict = {}
    for error in errors:
        add_error_to_dict(error_dict, error['loc'], error)
    return error_dict
