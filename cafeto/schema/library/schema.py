from typing import Any, Dict, List, Optional


class Schema:  # pragma: no cover
    def __init__(
            self,
            openapi_version: str,
            info: 'Info',
            tags: 'Tags',
            paths: 'Paths',
            components: 'Components',
            external_docs: Optional['ExternalDocs'] = None) -> None:
        self.openapi_version = openapi_version
        self.info = info
        self.external_docs = external_docs
        self.tags = tags
        self.paths = paths
        self.components = components

    def to_dict(self) -> Dict[str, Any]:
        data = {
            'openapi': self.openapi_version,
            'info': self.info.to_dict(),
            'tags': self.tags.to_dict(),
            'paths': self.paths.to_dict(),
            'components': self.components.to_dict()
        }

        if self.external_docs:
            data['externalDocs'] = self.external_docs.to_dict()

        return data


class Info:  # pragma: no cover
    def __init__(
            self,
            title: str,
            version: str,
            description: Optional[str] = None,
            terms_of_service: Optional[str] = None,
            contact: Optional['Contact'] = None,
            license: Optional['License'] = None) -> None:
        self.title = title
        self.version = version
        self.description = description
        self.terms_of_service = terms_of_service
        self.contact = contact
        self.license = license

    def to_dict(self) -> Dict[str, Any]:
        data = {
            'title': self.title,
            'version': self.version
        }

        if self.description:
            data['description'] = self.description

        if self.terms_of_service:
            data['termsOfService'] = self.terms_of_service

        if self.contact:
            data['contact'] = self.contact.__dict__

        if self.license:
            data['license'] = self.license.__dict__

        return data


class Contact:  # pragma: no cover
    def __init__(self, name: str, url: str, email: str) -> None:
        self.name = name
        self.url = url
        self.email = email


class License:  # pragma: no cover
    def __init__(self, name: str, url: str) -> None:
        self.name = name
        self.url = url


class ExternalDocs:  # pragma: no cover
    def __init__(self, description: str, url: str) -> None:
        self.description = description
        self.url = url

    def to_dict(self) -> Dict[str, str]:
        return {
            'description': self.description,
            'url': self.url
        }


class Tags:  # pragma: no cover
    def __init__(self) -> None:
        self.tags: List[Tag] = []

    def add_tag(self, tag: 'Tag') -> None:
        for tag_ in self.tags:
            if tag_.name == tag.name:
                return
        self.tags.append(tag)

    def to_dict(self) -> List[Dict[str, Any]]:
        return [tag.to_dict() for tag in self.tags]


class Tag:  # pragma: no cover
    def __init__(self, name: str, description: str, external_docs: Optional['ExternalDocs'] = None) -> None:
        self.name = name
        self.description = description
        self.external_docs = external_docs

    def to_dict(self) -> Dict[str, Any]:
        data = {
            'name': self.name,
            'description': self.description
        }

        if self.external_docs:
            data['externalDocs'] = self.external_docs.to_dict()

        return data


class Paths:  # pragma: no cover
    def __init__(self) -> None:
        self.paths: Dict[str, List[Path]] = {}
        self.url_path: str = ''

    def add_path(self, url_path: str, path: 'Path') -> None:
        if url_path not in self.paths:
            self.paths[url_path] = []
        self.paths[url_path].append(path)

    def to_dict(self) -> Dict[str, Dict[str, Any]]:
        paths = {}
        for key, value in self.paths.items():
            paths[key] = {}
            for path in value:
                if path.get:
                    paths[key]['get'] = path.get.to_dict()
                if path.put:
                    paths[key]['put'] = path.put.to_dict()
                if path.post:
                    paths[key]['post'] = path.post.to_dict()
                if path.delete:
                    paths[key]['delete'] = path.delete.to_dict()
                if path.options:
                    paths[key]['options'] = path.options.to_dict()
                if path.head:
                    paths[key]['head'] = path.head.to_dict()
                if path.patch:
                    paths[key]['patch'] = path.patch.to_dict()
                if path.trace:
                    paths[key]['trace'] = path.trace.to_dict()

        return paths


class Path:  # pragma: no cover
    def __init__(
            self,
            get: Optional['Operation'] = None,
            put: Optional['Operation'] = None,
            post: Optional['Operation'] = None,
            delete: Optional['Operation'] = None,
            options: Optional['Operation'] = None,
            head: Optional['Operation'] = None,
            patch: Optional['Operation'] = None,
            trace: Optional['Operation'] = None) -> None:
        self.get = get
        self.put = put
        self.post = post
        self.delete = delete
        self.options = options
        self.head = head
        self.patch = patch
        self.trace = trace

    def to_dict(self) -> Dict[str, Any]:
        data = {}

        if self.get:
            data['get'] = self.get.to_dict()

        if self.put:
            data['put'] = self.put.to_dict()

        if self.post:
            data['post'] = self.post.to_dict()

        if self.delete:
            data['delete'] = self.delete.to_dict()

        if self.options:
            data['options'] = self.options.to_dict()

        if self.head:
            data['head'] = self.head.to_dict()

        if self.patch:
            data['patch'] = self.patch.to_dict()

        if self.trace:
            data['trace'] = self.trace.to_dict()

        return data


class Operation:  # pragma: no cover
    def __init__(
            self,
            tags: List[str],
            summary: str,
            description: str,
            operation_id: str,
            responses: 'Responses',
            request_body: Optional['RequestBody'],
            parameters: Optional['Parameters'] = None,
            security: Optional['Security'] = None,
            callbacks: Optional[Dict[str, 'Callback']] = None,
            external_docs: Optional['ExternalDocs'] = None) -> None:
        self.tags = tags
        self.summary = summary
        self.description = description
        self.operation_id = operation_id
        self.responses = responses
        self.request_body = request_body
        self.parameters = parameters
        self.security = security
        self.callbacks = callbacks
        self.external_docs = external_docs

    def to_dict(self) -> Dict[str, Any]:
        data = {
            'tags': self.tags,
            'summary': self.summary,
            'description': self.description,
            'operationId': self.operation_id,
            'responses': self.responses.to_dict()
        }

        if self.request_body:
            data['requestBody'] = self.request_body.to_dict()

        if self.parameters:
            data['parameters'] = self.parameters.to_dict()

        if self.security:
            data['security'] = [self.security.to_dict()]

        if self.callbacks:
            data['callbacks'] = {key: value.to_dict() for key, value in self.callbacks.items()}

        if self.external_docs:
            data['externalDocs'] = self.external_docs.to_dict()

        return data


class Parameters:  # pragma: no cover
    def __init__(self) -> None:
        self.parameters: List[Parameter] = []

    def add_parameter(self, parameter: 'Parameter') -> None:
        self.parameters.append(parameter)

    def to_dict(self) -> List[Dict[str, Any]]:
        return [parameter.to_dict() for parameter in self.parameters]


class Parameter:  # pragma: no cover
    def __init__(
            self,
            name: str,
            in_: str,
            required: bool,
            schema: 'ParameterSchema',
            default: Optional[Any] = None,
            description: Optional[str] = None) -> None:
        self.name = name
        self.in_ = in_
        self.required = required
        self.schema = schema
        self.default = default
        self.description = description

    def to_dict(self) -> Dict[str, Any]:
        data = {
            'name': self.name,
            'in': self.in_,
            'required': self.required,
            'schema': self.schema.to_dict()
        }

        if self.default:
            data['default'] = self.default

        if self.description:
            data['description'] = self.description

        return data


class ParameterSchema:  # pragma: no cover
    def __init__(self, type: str, format: str) -> None:
        self.type = type
        self.format = format

    def to_dict(self) -> Dict[str, str]:
        return {
            'type': self.type,
            'format': self.format
        }


class RequestBody:  # pragma: no cover
    def __init__(self, content: 'RequestBodyMediaType', description: Optional[str], required: bool = True) -> None:
        self.description = description
        self.content = content
        self.required = required

    def to_dict(self) -> Dict[str, Any]:
        data = {
            'content': self.content.to_dict(),
            'required': self.required
        }

        if self.description:
            data['description'] = self.description

        return data


class RequestBodyMediaType:  # pragma: no cover
    def __init__(self, name: str, schema: 'RequestBodySchema') -> None:
        self.name = name
        self.schema = schema

    def to_dict(self) -> Dict[str, Any]:
        return {
            self.name: {
                'schema': self.schema.to_dict()
            }
        }


class RequestBodySchema:  # pragma: no cover
    def __init__(
            self,
            type: Optional[str] = None,
            format: Optional[str] = None,
            ref: Optional[str] = None,
            properties: Dict[str, 'RequestBodySchema'] = None
            ) -> None:
        self.type = type
        self.format = format
        self.ref = ref
        self.properties = properties

    def to_dict(self) -> Dict[str, Any]:
        data = {}
        if self.type:
            data['type'] = self.type
        if self.format:
            data['format'] = self.format
        if self.ref:
            data['$ref'] = self.ref
        if self.properties:
            data['properties'] = {key: value.to_dict() for key, value in self.properties.items()}

        return data


class Responses:  # pragma: no cover
    def __init__(self) -> None:
        self.responses: List[Response] = []

    def add_response(self, response: 'Response') -> None:
        self.responses.append(response)

    def to_dict(self) -> Dict[str, Dict[str, Any]]:
        return {response.status_code: response.content.to_dict() for response in self.responses}


class Response:  # pragma: no cover
    def __init__(self, status_code: str, content: 'ResponseContent') -> None:
        self.status_code = status_code
        self.content = content

    def to_dict(self) -> Dict[str, Any]:
        return {
            self.status_code: self.content.to_dict()
        }


class ResponseContent:  # pragma: no cover
    def __init__(self, description: str, content: Optional[Dict[str, 'ResponseMediaType']] = None) -> None:
        self.description = description
        self.content = content

    def to_dict(self) -> Dict[str, Any]:
        data = {
            'description': self.description,
        }

        if self.content:
            data['content'] = {key: value.to_dict() for key, value in self.content.items()}

        return data


class ResponseMediaType:  # pragma: no cover
    def __init__(self, schema: 'ResponseSchema') -> None:
        self.schema = schema

    def to_dict(self) -> Dict[str, Any]:
        return {
            'schema': self.schema.to_dict()
        }


class ResponseSchema:  # pragma: no cover
    def __init__(
            self,
            type: Optional[str] = None,
            format: Optional[str] = None,
            ref: Optional[str] = None,
            additional_properties: Optional[bool] = None,
            items: Optional['ResponseSchema'] = None
            ) -> None:
        self.type = type
        self.format = format
        self.ref = ref
        self.additional_properties = additional_properties
        self.items = items

    def to_dict(self) -> Dict[str, str]:
        data = {}
        if self.type:
            data['type'] = self.type
        if self.format:
            data['format'] = self.format
        if self.ref:
            data['$ref'] = self.ref
        if self.additional_properties:
            data['additionalProperties'] = self.additional_properties
        if self.items:
            data['items'] = self.items.to_dict()

        return data


class Callback:  # pragma: no cover
    def __init__(self, expression: str, callback: Dict[str, 'CallbackPathItem']) -> None:
        self.expression = expression
        self.callback = callback

    def to_dict(self) -> Dict[str, Dict[str, Any]]:
        return {self.expression: self.callback.to_dict()}


class CallbackPathItem:  # pragma: no cover
    def __init__(
            self,
            summary: str,
            description: str,
            get: Optional['Operation'] = None,
            put: Optional['Operation'] = None,
            post: Optional['Operation'] = None,
            delete: Optional['Operation'] = None,
            options: Optional['Operation'] = None,
            head: Optional['Operation'] = None,
            patch: Optional['Operation'] = None,
            trace: Optional['Operation'] = None,
            parameters: Optional[List['Parameter']] = None) -> None:
        self.summary = summary
        self.description = description
        self.get = get
        self.put = put
        self.post = post
        self.delete = delete
        self.options = options
        self.head = head
        self.patch = patch
        self.trace = trace
        self.parameters = parameters

    def to_dict(self) -> Dict[str, Any]:
        data = {
            'summary': self.summary,
            'description': self.description
        }

        if self.get:
            data['get'] = self.get.to_dict()

        if self.put:
            data['put'] = self.put.to_dict()

        if self.post:
            data['post'] = self.post.to_dict()

        if self.delete:
            data['delete'] = self.delete.to_dict()

        if self.options:
            data['options'] = self.options.to_dict()

        if self.head:
            data['head'] = self.head.to_dict()

        if self.patch:
            data['patch'] = self.patch.to_dict()

        if self.trace:
            data['trace'] = self.trace.to_dict()

        if self.parameters:
            data['parameters'] = [parameter.to_dict() for parameter in self.parameters]

        return data


class Security:  # pragma: no cover
    def __init__(self, name: str, scopes: List[str] = []) -> None:
        self.name = name
        if isinstance(scopes, str):
            self.scopes = [scopes]
        else:
            self.scopes = scopes

    def to_dict(self) -> Dict[str, List[str]]:
        return {self.name: self.scopes}


class Components:  # pragma: no cover
    def __init__(self) -> None:
        self.schemas: ComponentSchemas = ComponentSchemas()
        self.security_schemes: Optional['SecurityScheme'] = None
        self.callbacks: Optional[Dict[str, 'Callback']] = None

    def to_dict(self) -> Dict[str, Any]:
        data = {
            'schemas': self.schemas.to_dict()
        }

        if self.security_schemes:
            data['securitySchemes'] = {self.security_schemes.name: self.security_schemes.to_dict()}

        if self.callbacks:
            data['callbacks'] = {key: value.to_dict() for key, value in self.callbacks.items()}

        return data


class ComponentSchemas(Dict[str, 'ComponentSchema']):  # pragma: no cover
    def to_dict(self) -> Dict[str, Dict[str, Any]]:
        return {key: value.to_dict() for key, value in self.items()}


class ComponentSchema:  # pragma: no cover
    def __init__(
            self,
            type: str,
            properties: Dict[str, Any],
            defs: Optional[Dict[str, Any]] = None,
            required: Optional[List[str]] = []
            ) -> None:
        self.type: str = type
        self.properties: Dict[str, Any] = properties
        self.defs: Optional[Dict[str, Any]] = defs
        self.required: Optional[List[str]] = required

    @staticmethod
    def adjust_properties(properties: dict) -> dict:
        for _, prop_schema in properties.items():
            if 'title' in prop_schema:
                del prop_schema['title']

            if 'anyOf' in prop_schema:
                for any_of in prop_schema['anyOf']:
                    if any_of.get('type') == 'null':
                        continue
                    elif '$ref' in any_of:
                        prop_schema['$ref'] = any_of['$ref']
                        prop_schema['default'] = None
                        del prop_schema['anyOf']
                        break
                    elif 'items' in any_of:
                        if any_of['items'].get('$ref', None):
                            prop_schema['items'] = {
                                '$ref': any_of['items']['$ref']
                            }
                        else:
                            prop_schema['items'] = any_of['items']
                        prop_schema['type'] = 'array'
                        del prop_schema['anyOf']
                        if 'default' in prop_schema:
                            del prop_schema['default']
                        break
                    elif 'type' in any_of:
                        prop_schema['type'] = any_of['type']
                        if 'default' in any_of:
                            prop_schema['default'] = any_of['default']
                        del prop_schema['anyOf']
                        break
        return properties

    def to_dict(self) -> Dict[str, Any]:
        data = {
            'type': self.type
        }

        if self.properties:
            data['properties'] = ComponentSchema.adjust_properties(self.properties)

        if self.defs:
            data['$defs'] = self.defs

        if self.required:
            data['required'] = self.required

        return data


class SecurityScheme:  # pragma: no cover
    def __init__(
            self,
            type: str,
            name: Optional[str] = None,
            in_: Optional[str] = None,
            scheme: Optional[str] = None,
            bearer_format: Optional[str] = None,
            flows: Optional['OAuthFlows'] = None) -> None:
        self.type = type
        self.name = name
        self.in_ = in_
        self.scheme = scheme
        self.bearer_format = bearer_format
        self.flows = flows

    def to_dict(self) -> Dict[str, Any]:
        data = {
            'type': self.type
        }

        if self.name:
            data['name'] = self.name

        if self.in_:
            data['in'] = self.in_

        if self.scheme:
            data['scheme'] = self.scheme

        if self.bearer_format:
            data['bearerFormat'] = self.bearer_format

        if self.flows:
            data['flows'] = self.flows.to_dict()

        return data


class OAuthFlows:  # pragma: no cover
    def __init__(
            self,
            implicit: Optional['OAuthFlow'] = None,
            password: Optional['OAuthFlow'] = None,
            client_credentials: Optional['OAuthFlow'] = None,
            authorization_code: Optional['OAuthFlow'] = None) -> None:
        self.implicit = implicit
        self.password = password
        self.client_credentials = client_credentials
        self.authorization_code = authorization_code

    def to_dict(self) -> Dict[str, Any]:
        data = {}

        if self.implicit:
            data['implicit'] = self.implicit.to_dict()

        if self.password:
            data['password'] = self.password.to_dict()

        if self.client_credentials:
            data['clientCredentials'] = self.client_credentials.to_dict()

        if self.authorization_code:
            data['authorizationCode'] = self.authorization_code.to_dict()

        return data


class OAuthFlow:  # pragma: no cover
    def __init__(self, authorization_url: str, token_url: str, refresh_url: str, scopes: Dict[str, str]) -> None:
        self.authorization_url = authorization_url
        self.token_url = token_url
        self.refresh_url = refresh_url
        self.scopes = scopes

    def to_dict(self) -> Dict[str, Any]:
        return {
            'authorizationUrl': self.authorization_url,
            'tokenUrl': self.token_url,
            'refreshUrl': self.refresh_url,
            'scopes': self.scopes
        }
