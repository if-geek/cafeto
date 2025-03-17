# flake8: noqa

from typing import Generic, TypeVar

from cafeto.models.base_model import BaseModel


TData = TypeVar('TData')

class GenericResponseDto(BaseModel, Generic[TData]):
    data: TData

