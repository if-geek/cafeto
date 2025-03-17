class DefaultDocs:
    """
    A class to hold default documentation values for the API.

    Attributes:
        openapi_version (str): The version of the OpenAPI specification.
        title (str): The title of the API.
        version (str): The version of the API.
        controller_description (str): A default description for the controller.
        action_summary (str): A default summary for actions.
        action_description (str): A default description for actions.
        action_description_response (str): A default description for successful responses.
        action_status_code (str): A default status code for actions.
    """
    openapi_version: str = '3.0.0'
    title: str = 'Project API'
    version: str = '1.0.0'
    controller_description: str = 'No description'
    action_summary: str = 'No summary'
    action_description: str = 'No description'
    action_description_response: str = 'Successful response'
    action_status_code: str = '200'
