from typing import Any, Type, get_origin, Union
from datetime import date, time, datetime
import uuid

from cafeto.models.base_model import BaseModel
from cafeto.types import TData


class ModelCreator:
    """
    A class responsible for creating and validating models.

    Attributes:
        dependency_injection (Optional[DependencyInjection]):  An optional dependency injection instance.
    """

    def create(self, cls: Type[BaseModel], **data: TData) -> BaseModel:
        """
        Creates an instance of the specified model class with the provided data.

        Args:
            cls (Type[BaseModel]): The class of the model to be created.
            **data (TData): Arbitrary keyword arguments representing the data to initialize the model with.

        Returns:
            BaseModel: An instance of the specified model class.
        """
        model = self.__model_construct(cls, **data)
        return model

    def __get_basics(self, annotation: Type, value: Any) -> Any:
        """
        Converts a value to a specific type based on the provided annotation.

        Args:
            annotation (Type): The type to which the value should be converted.
            value (Any): The value to be converted.

        Returns:
            Any: The converted value if the annotation matches a known type (date, time, datetime, uuid.UUID),
                 otherwise returns the original value.
        """
        if annotation == date:
            return date.fromisoformat(value)
        elif annotation == time:
            return time.fromisoformat(value)
        elif annotation == datetime:
            return datetime.fromisoformat(value)
        elif annotation == uuid.UUID:
            return uuid.UUID(value)
        return value  # pragma: no cover

    def __model_construct(self, cls: type[BaseModel], **data: TData) -> BaseModel:
        """
        Constructs a model instance of the given class type with the provided data.
        This method processes the input data to ensure it matches the expected types
        defined in the model fields. It handles nested models, lists, and dictionaries,
        converting them as necessary to the appropriate types.

        Args:
            cls (type[BaseModel]): The class type of the model to construct.
            **data (TData): The data to populate the model with.

        Returns:
            BaseModel: An instance of the model class populated with the provided data.

        Raises:
            TypeError: If the provided data does not match the expected types.
        """
        for name, field in cls.model_fields.items():
            if name not in data:
                data[name] = None
                continue

            annotation = get_origin(field.annotation)
            field_annotation = field.annotation

            if annotation is None:
                annotation = field.annotation

            if annotation == Union:
                annotation = get_origin(field.annotation.__args__[0])
                if annotation is not None:
                    field_annotation = field.annotation.__args__[0]

            if annotation in [date, time, datetime, uuid.UUID]:
                if data.get(name):
                    data[name] = self.__get_basics(annotation, data[name])
            elif annotation == list:
                if data.get(name):
                    if len(field_annotation.__args__) > 0:
                        list_type = field_annotation.__args__[0]
                        if issubclass(list_type, BaseModel):
                            data[name] = [self.__model_construct(list_type, **item) for item in data[name]]
                        if list_type in [date, time, datetime, uuid.UUID]:
                            data[name] = [self.__get_basics(list_type, item) for item in data[name]]
            elif annotation == dict:
                if data.get(name):
                    if len(field_annotation.__args__) > 0:
                        dict_type = field_annotation.__args__[1]
                        if issubclass(dict_type, BaseModel):
                            data[name] = {
                                key: self.__model_construct(dict_type, **item) for key, item in data[name].items()
                            }
                        if dict_type in [date, time, datetime, uuid.UUID]:
                            data[name] = {
                                key: self.__get_basics(dict_type, item) for key, item in data[name].items()
                            }
            elif issubclass(annotation, BaseModel):
                if data.get(name) or data.get(name) == {}:
                    data[name] = self.__model_construct(annotation, **data[name])

        return cls.model_construct(**data)
