from typing import ClassVar

class FORMAT:  # noqa
    """
    Base class for all response formats.
    Attributes:
        value (str): The format value.
    """
    value: ClassVar[str]

class APPLICATION_JSON(FORMAT):  # noqa
    """
    Represents the JSON response format.
    Attributes:
        value (str): The format value ('application/json').
    """
    value: ClassVar[str] = 'application/json'

class TEXT_HTML(FORMAT):  # noqa
    """
    Represents the HTML response format.
    Attributes:
        value (str): The format value ('text/html').
    """
    value: ClassVar[str] = 'text/html'

class TEXT_PLAIN(FORMAT):  # noqa
    """
    Represents the plain text response format.
    Attributes:
        value (str): The format value ('text/plain').
    """
    value: ClassVar[str] = 'text/plain'

class APPLICATION_XML(FORMAT):  # noqa
    """
    Represents the XML response format.
    Attributes:
        value (str): The format value ('application/xml').
    """
    value: ClassVar[str] = 'application/xml'

class TEXT_CSV(FORMAT):  # noqa
    """
    Represents the CSV response format.
    Attributes:
        value (str): The format value ('text/csv').
    """
    value: ClassVar[str] = 'text/csv'

class APPLICATION_OCTET_STREAM(FORMAT):  # noqa
    """
    Represents the binary response format.
    Attributes:
        value (str): The format value ('application/octet-stream').
    """
    value: ClassVar[str] = 'application/octet-stream'

class MULTIPART_FORM_DATA(FORMAT):  # noqa
    """
    Represents the multipart form data response format.
    Attributes:
        value (str): The format value ('multipart/form-data').
    """
    value: ClassVar[str] = 'multipart/form-data'
