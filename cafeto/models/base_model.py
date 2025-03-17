from __future__ import annotations

from typing import Any, Dict, List, Optional, Type
from pydantic import BaseModel as PydanticBaseModel
from pydantic.main import IncEx

from cafeto import models
from cafeto.errors import errors as Err
from cafeto.models import validator_collection as VC
from cafeto import types


def validate(field: Optional[str] = '__model__'):
    """
    A decorator to register a validation function for a specific field.

    Args:
        field (Optional[str]): The name of the field to validate. Defaults to '__model__'.
    Returns:
        function: A decorator that registers the validation function with the ValidatorCollection.
    """

    def decorator(func):
        VC.ValidatorCollection.add_validation(field, func)
        return staticmethod(func)
    return decorator


class BaseModel(PydanticBaseModel):
    """
    BaseModel class that extends PydanticBaseModel.
    This class is used for Data Transfer Objects (DTOs) on request and response actions.
    """

    def __init_subclass__(cls, **kwargs):
        """
        This method is automatically called when a class is subclassed.

        Args:
            cls (type): The subclass being initialized.
            **kwargs: Arbitrary keyword arguments passed to the superclass initializer.

        This method performs the following actions:
        1. Calls the superclass's __init_subclass__ method with the provided keyword arguments.
        2. Calls the set_parent_validations method on the subclass to inherit all validations on models.
        """
        super().__init_subclass__(**kwargs)
        cls.set_parent_validations()

    @staticmethod
    def model_dump_json_many(
        data: List['BaseModel'],
        include: Optional[IncEx] = None,
        exclude: Optional[IncEx] = None
    ) -> str:
        """
        Serializes a list of BaseModel instances to a JSON string.

        Args:
            data (List['BaseModel']): A list of BaseModel instances to be serialized.
            include (Optional[IncEx], optional): Fields to include in the serialization. Defaults to None.
            exclude (Optional[IncEx], optional): Fields to exclude from the serialization. Defaults to None.

        Returns:
            str: A JSON string representing the list of BaseModel instances.
        """
        result: List[str] = [item.model_dump_json(include=include, exclude=exclude) for item in data]
        return '[' + ','.join(result) + ']'

    @classmethod
    def create(
        cls,
        data: types.TData,
    ) -> 'BaseModel':
        """
        Create an instance of the model using the provided data.

        This method overrides the default Pydantic model creation.
        When Pydantic tries to create a model and a validation fails, the model is not created.
        With this method, the model is created regardless of validation errors, which is helpful
        because you can perform your validations later.
        Additionally, all fields are formatted according to the type annotations in the model.

        Args:
            cls: The class of the model to be created.
            data (types.TData): The data to be used for creating the model instance.

        Returns:
            BaseModel: An instance of the model created using the provided data.
        """
        from cafeto.models.model_creator import ModelCreator

        creator = ModelCreator()
        return creator.create(cls, **data)

    async def check(self, custom_validator: Optional[Type[models.BaseValidator]] = None) -> 'BaseModel':
        """
        Asynchronously checks the model instance using custom and default validators.

        Args:
            custom_validator (Optional[Type[model.BaseValidator]]): An optional custom validator class to use
            for validation.

        Returns:
            BaseModel: The validated model instance.

        Raises:
            Err.ModelError: If any validation errors are encountered.
        """
        from cafeto.models.model_validator import ModelValidator

        validator: ModelValidator = ModelValidator()

        errors = []
        try:
            self = await validator.validate_customs([], self, custom_validator)
        except Err.ModelError as e:
            errors.extend(e.errors)

        try:
            self = validator.validate_model([], self)
        except Err.ModelError as e:
            errors.extend(e.errors)

        if errors:
            raise Err.ModelError(errors)

    def model_response(self) -> Dict[str, Any]:
        """
        Generates a response for the model in JSON format.

        Returns:
            Dict[str, Any]: A dictionary containing the model's response in JSON format.
        """
        return self.model_dump(mode='json')

    @classmethod
    def set_parent_validations(cls):
        """
        Sets the parent validations for the given class.

        This method delegates the task of setting parent validations to the
        ValidatorCollection's set_parent_validations method.

        Args:
            cls (type): The class for which to set parent validations.
        """
        VC.ValidatorCollection.set_parent_validations(cls)


class BaseValidator:
    """
    BaseValidator is a base class for validators that provides a mechanism to set up
    parent validations when a subclass is created.

    This class is an alternative to validate data on DTOs (Data Transfer Objects).
    """

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.set_parent_validations()

    @classmethod
    def set_parent_validations(cls):
        VC.ValidatorCollection.set_parent_validations(cls)
