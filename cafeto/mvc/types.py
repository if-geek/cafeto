from typing import Any, Dict, List, Protocol, TypeVar, Union

from cafeto.mvc.endpoint import Endpoint
from cafeto.authentication.requires import Requires
from cafeto.models import BaseModel

RequestModel = TypeVar('RequestModel', bound=BaseModel)
RequestBody = TypeVar('RequestBody', bound=Dict[str, Any])
ResponseModel = TypeVar('ResponseModel', bound=BaseModel)
ResponseBody = TypeVar(
    'ResponseBody',
    bound=Union[ResponseModel, List[ResponseModel | Any], Dict[str, ResponseModel | Any], None]
    )


class ActionEndPoint(Protocol):
    endpoint: Endpoint = None
    requires: Requires = None

    def __call__(self, *args: Any, **kwargs: Any) -> Any: ...


Action = TypeVar('Action', bound=ActionEndPoint)
