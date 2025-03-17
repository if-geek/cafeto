from typing import ClassVar


class STATUS_CODE:  # noqa
    """
    Base class for all status codes.
    Attributes:
        value (int): The status code value.
    """
    value: ClassVar[int]

class CODE_200_OK(STATUS_CODE):  # noqa
    """
    Represents HTTP status code 200 OK.
    Attributes:
        value (int): The status code value (200).
    """
    value: ClassVar[int] = 200

class CODE_201_CREATED(STATUS_CODE):  # noqa
    """
    Represents HTTP status code 201 Created.
    Attributes:
        value (int): The status code value (201).
    """
    value: ClassVar[int] = 201

class CODE_204_NO_CONTENT(STATUS_CODE):  # noqa
    """
    Represents HTTP status code 204 No Content.
    Attributes:
        value (int): The status code value (204).
    """
    value: ClassVar[int] = 204

class CODE_400_BAD_REQUEST(STATUS_CODE):  # noqa
    """
    Represents HTTP status code 400 Bad Request.
    Attributes:
        value (int): The status code value (400).
    """
    value: ClassVar[int] = 400

class CODE_401_UNAUTHORIZED(STATUS_CODE):  # noqa
    """
    Represents HTTP status code 401 Unauthorized.
    Attributes:
        value (int): The status code value (401).
    """
    value: ClassVar[int] = 401

class CODE_403_FORBIDDEN(STATUS_CODE):  # noqa
    """
    Represents HTTP status code 403 Forbidden.
    Attributes:
        value (int): The status code value (403).
    """
    value: ClassVar[int] = 403

class CODE_404_NOT_FOUND(STATUS_CODE):  # noqa
    """
    Represents HTTP status code 404 Not Found.
    Attributes:
        value (int): The status code value (404).
    """
    value: ClassVar[int] = 404

class CODE_405_METHOD_NOT_ALLOWED(STATUS_CODE):  # noqa
    """
    Represents HTTP status code 405 Method Not Allowed.
    Attributes:
        value (int): The status code value (405).
    """
    value: ClassVar[int] = 405

class CODE_409_CONFLICT(STATUS_CODE):  # noqa
    """
    Represents HTTP status code 409 Conflict.
    Attributes:
        value (int): The status code value (409).
    """
    value: ClassVar[int] = 409

class CODE_500_INTERNAL_SERVER_ERROR(STATUS_CODE):  # noqa
    """
    Represents HTTP status code 500 Internal Server Error.
    Attributes:
        value (int): The status code value (500).
    """
    value: ClassVar[int] = 500

class CODE_501_NOT_IMPLEMENTED(STATUS_CODE):  # noqa
    """
    Represents HTTP status code 501 Not Implemented.
    Attributes:
        value (int): The status code value (501).
    """
    value: ClassVar[int] = 501

class CODE_503_SERVICE_UNAVAILABLE(STATUS_CODE):  # noqa
    """
    Represents HTTP status code 503 Service Unavailable.
    Attributes:
        value (int): The status code value (503).
    """
    value: ClassVar[int] = 503

class CODE_504_GATEWAY_TIMEOUT(STATUS_CODE):  # noqa
    """
    Represents HTTP status code 504 Gateway Timeout.
    Attributes:
        value (int): The status code value (504).
    """
    value: ClassVar[int] = 504
