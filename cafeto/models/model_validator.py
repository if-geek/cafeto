import asyncio
from typing import Any, Callable, Dict, List, Optional, Type

from pydantic import ValidationError

from cafeto import models
from cafeto.dependency_injection.service_provider import ServiceProvider
from cafeto.errors.errors import Error, FieldError, ModelError
from cafeto.models.base_model import BaseModel
from cafeto.models.validator_collection import ValidatorCollection
from cafeto.types import TLoc


class ModelValidator:
    """
    A class used to validate models with custom validation logic.

    This class uses all information collected with the @validation decorator to perform validations.
    Also validate the model with Pydantic standard method.
    """

    async def validate_customs(
            self,
            loc: TLoc,
            model: BaseModel,
            custom_validator: Optional[Type[models.BaseValidator]] = None
            ) -> BaseModel:
        """
        Validates the fields and nested fields of a given model using custom validators.
        This method use the @validation decorator to get the custom validators.

        Args:
            loc (TLoc): The location context for validation.
            model (BaseModel): The model instance to be validated.
            custom_validator (Optional[Type[model.BaseValidator]]): An optional custom validator class.

        Returns:
            BaseModel: The validated model instance.

        Raises:
            ModelError: If any validation errors are found.
        """
        errors = []

        if custom_validator:
            validator_module_name: str = f'{custom_validator.__module__}.{custom_validator.__name__}'
        else:
            validator_module_name: str = f'{model.__class__.__module__}.{model.__class__.__name__}'

        for field, value in model.__dict__.items():
            if (
                validator_module_name in ValidatorCollection.validations
                and field in ValidatorCollection.validations[validator_module_name]
            ):
                field_errors = await self.__validate_customs_field(
                    loc,
                    model,
                    field,
                    value,
                    validator_module_name,
                    custom_validator
                    )
                errors.extend(field_errors)
            else:
                nested_errors = await self.__validate_customs_nested(loc, field, value, custom_validator)
                errors.extend(nested_errors)

        model_errors = await self.__validate_customs_model(loc, model, validator_module_name, custom_validator)
        errors.extend(model_errors)

        if errors:
            raise ModelError(errors)

        return model

    async def __validate_customs_field(
            self,
            loc: TLoc,
            model: BaseModel,
            field: str,
            value: Any,
            validator_module_name: str,
            custom_validator: Optional[Type[models.BaseValidator]] = None
            ) -> List[Dict[str, Any]]:
        """
        Validates a custom field in a model.
        Validate all methods in the model with a @validation decorator associated with a field.

        Example:
            @validation('field_name')
            def validate_field_name(value: str, data: Dict[str, Any]) -> Any:
                if value == 'nope':
                    raise FieldError(Error(type='my-custom-type', msg='Field value is invalid'))
                return value

        Args:
            loc (TLoc): The location of the field in the model.
            model (BaseModel): The model instance containing the field.
            field (str): The name of the field to validate.
            value (Any): The value of the field to validate.
            validator_module_name (str): The name of the validator module.
            custom_validator (Optional[Type[model.BaseValidator]]): An optional custom validator class.

        Returns:
            List[Dict[str, Any]]: A list of error dictionaries, if any.

        Raises:
            FieldError: If a field-specific validation error occurs.
            ModelError: If a model-specific validation error occurs.
        """
        errors = []

        if model.model_fields[field].is_required() and value is None:  # pragma: no cover
            return errors

        validator_name: str = ValidatorCollection.validations[validator_module_name][field]

        if custom_validator:
            validator: Callable = getattr(custom_validator, validator_name, None)
        else:
            validator: Callable = getattr(model, validator_name, None)

        dependencies = self.__resolve_dependencies(validator)

        try:
            if issubclass(type(value), BaseModel):
                nested_errors = await self.__validate_basemodel(loc, field, value, custom_validator)
                errors.extend(nested_errors)
            if asyncio.iscoroutinefunction(validator):
                model.__dict__[field] = await validator(value, model.__dict__, **dependencies)
            else:
                model.__dict__[field] = validator(value, model.__dict__, **dependencies)
        except FieldError as e:
            errors.append({'loc': loc + [field], 'type': e.error['type'], 'msg': e.error['msg']})
        except ModelError as e:  # pragma: no cover
            errors.extend(self.__collect_model_errors(loc, field, e))

        return errors

    async def __validate_customs_nested(
            self,
            loc: TLoc,
            field: str,
            value: Any,
            custom_validator: Optional[Type[models.BaseValidator]] = None
            ) -> List[Dict[str, Any]]:
        """
        Validates nested custom fields within a given value.

        This method checks if the provided value is a list, dictionary, or an instance of BaseModel,
        and validates it accordingly using the appropriate validation method.

        Args:
            loc (TLoc): The location context for the validation.
            field (str): The name of the field being validated.
            value (Any): The value to be validated.
            custom_validator (Optional[Type[model.BaseValidator]]): An optional custom validator class.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing validation errors, if any.
        """
        errors = []
        if isinstance(value, list):
            list_errors = await self.__validate_list(loc, field, value, custom_validator)
            errors.extend(list_errors)
        elif isinstance(value, dict):
            dict_errors = await self.__validate_dict(loc, field, value, custom_validator)
            errors.extend(dict_errors)
        elif issubclass(type(value), BaseModel):
            basemodel_errors = await self.__validate_basemodel(loc, field, value, custom_validator)
            errors.extend(basemodel_errors)
        return errors

    async def __validate_list(
            self,
            loc: TLoc,
            field: str,
            value: List[Any],
            custom_validator: Optional[Type[models.BaseValidator]] = None
            ) -> List[Dict[str, Any]]:
        """
        Validates a list of items, optionally using a custom validator.

        Args:
            loc (TLoc): The location of the field being validated.
            field (str): The name of the field being validated.
            value (List[Any]): The list of items to validate.
                This list may contain nested models.
            custom_validator (Optional[Type[model.BaseValidator]], optional): A custom validator to use for
                validation. Defaults to None.

        Returns:
            List[Dict[str, Any]]: A list of error dictionaries, if any validation errors are found.

        Raises:
            ModelError: If validation fails for any item in the list.
        """
        errors = []
        for i, item in enumerate(value):
            if isinstance(item, BaseModel):
                try:
                    if custom_validator:
                        await self.validate_customs(
                            loc + [field, i],
                            item,
                            custom_validator.__annotations__.get(field, None)
                            )
                    else:
                        await self.validate_customs(loc + [field, i], item)
                except ModelError as e:
                    errors.extend(e.errors)
        return errors

    async def __validate_dict(
            self,
            loc: TLoc,
            field: str,
            value: Dict[Any, Any],
            custom_validator: Optional[Type[models.BaseValidator]] = None
            ) -> List[Dict[str, Any]]:
        """
        Validates a dictionary of values, optionally using a custom validator.

        Args:
            loc (TLoc): The location of the field being validated.
            field (str): The name of the field being validated.
            value (Dict[Any, Any]): The dictionary of values to validate.
                This list may contain nested models.
            custom_validator (Optional[Type[model.BaseValidator]], optional): A custom validator class to use for
                validation. Defaults to None.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing validation errors, if any.
        """
        errors = []
        for key, item in value.items():
            if isinstance(item, BaseModel):
                try:
                    if custom_validator:
                        await self.validate_customs(
                            loc + [field, key],
                            item,
                            custom_validator.__annotations__.get(field, None)
                            )
                    else:
                        await self.validate_customs(loc + [field, key], item)
                except ModelError as e:
                    errors.extend(e.errors)
        return errors

    async def __validate_basemodel(
            self,
            loc: TLoc,
            field: str,
            value: BaseModel,
            custom_validator: Optional[Type[models.BaseValidator]] = None
            ) -> List[Dict[str, Any]]:
        """
        Validates a BaseModel instance using either a custom validator or the default validation logic.

        Args:
            loc (TLoc): The location context for the validation.
            field (str): The name of the field being validated.
            value (BaseModel): The BaseModel instance to validate.
            custom_validator (Optional[Type[model.BaseValidator]], optional): A custom validator class to use for
                validation. Defaults to None.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing validation errors, if any.
        """
        errors = []
        try:
            if custom_validator:
                await self.validate_customs(loc + [field], value, custom_validator.__annotations__.get(field, None))
            else:
                await self.validate_customs(loc + [field], value)
        except ModelError as e:
            errors.extend(e.errors)
        return errors

    async def __validate_customs_model(
            self,
            loc: TLoc,
            model: BaseModel,
            validator_module_name: str,
            custom_validator: Optional[Type[models.BaseValidator]] = None
            ) -> List[Dict[str, Any]]:
        """
        Validates a custom model using a specified validator.

        Args:
            loc (TLoc): The location context for the validation.
            model (BaseModel): The model instance to be validated.
            validator_module_name (str): The name of the validator module.
            custom_validator (Optional[Type[model.BaseValidator]], optional): A custom validator class. Defaults
                to None.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing validation errors, if any.
        """
        errors = []
        if (
            validator_module_name in ValidatorCollection.validations
            and ValidatorCollection.validations[validator_module_name].get('__model__', None)
        ):
            validator_name: str = ValidatorCollection.validations[validator_module_name]['__model__']

            if custom_validator:
                validator: Callable = getattr(custom_validator, validator_name, None)
            else:
                validator: Callable = getattr(model, validator_name, None)

            dependencies = self.__resolve_dependencies(validator)

            try:
                if asyncio.iscoroutinefunction(validator):
                    model.__dict__ = await validator(model.__dict__, **dependencies)
                else:
                    model.__dict__ = validator(model.__dict__, **dependencies)
            except ModelError as e:
                errors.extend(self.__collect_model_errors(loc, '__model__', e))
        return errors

    def __resolve_dependencies(self, validator: Callable) -> Dict[str, Any]:
        """
        Resolves the dependencies required by the given validator.

        Args:
            validator (Callable): The validator function or class whose dependencies need to be resolved.

        Returns:
            Dict[str, Any]: A dictionary containing the resolved dependencies.
        """
        return ServiceProvider.resolve(validator)

    def __collect_model_errors(self, loc: TLoc, field: str, model_error: ModelError) -> List[Dict[str, Any]]:
        """
        Collects model errors and returns them as a list of dictionaries.

        Args:
            loc (TLoc): The location context for the validation.
            field (str): The name of the field being validated.
            e (ModelError): The ModelError instance containing the errors.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing validation errors.
        """
        errors = []
        for error in model_error.errors:
            if 'loc' not in error:
                error['loc'] = loc + [field]
            elif loc != '__model__':
                error['loc'] = loc + error['loc']
            errors.append(error)
        return errors

    def validate_model(self, loc: TLoc, model: BaseModel) -> BaseModel:
        """
        Validates the given model by checking its fields, lists, and dictionaries for errors.
        In depth, this method uses the standard Pydantic validation method.

        Args:
            loc (TLoc): The location context for validation.
            model (BaseModel): The model instance to be validated.

        Returns:
            BaseModel: The validated model instance.

        Raises:
            ModelError: If any validation errors are found.
        """
        errors: List[Error] = []

        for field, value in model.__dict__.items():
            if isinstance(value, list):
                list_errors = self.__validate_customs_model_list(loc, field, value)
                errors.extend(list_errors)
            elif isinstance(value, dict):
                dict_errors = self.__validate_customs_model_dict(loc, field, value)
                errors.extend(dict_errors)
            elif issubclass(type(model.__dict__[field]), BaseModel):
                basemodel_errors = self.__validate_customs_model_basemodel(loc, field, value)
                errors.extend(basemodel_errors)

        field_errors = self.__validate_customs_model_fields(loc, model)
        errors.extend(field_errors)

        if errors:
            raise ModelError(errors)

        return model

    def __validate_customs_model_list(self, loc: TLoc, field: str, value: List[Any]) -> List[Error]:
        """
        Validates a list of models.

        Args:
            loc (TLoc): The location of the field being validated.
            field (str): The name of the field being validated.
            value (List[Any]): The list of items to be validated.

        Returns:
            List[Error]: A list of errors found during validation.
        """
        errors = []
        for i, item in enumerate(value):
            if issubclass(type(item), BaseModel):
                try:
                    self.validate_model(loc + [field, i], item)
                except ModelError as e:
                    errors.extend(e.errors)
        return errors

    def __validate_customs_model_dict(self, loc: TLoc, field: str, value: Dict[Any, Any]) -> List[Error]:
        """
        Validates a dictionary of custom models.

        This method iterates over the items in the provided dictionary and validates each item if it is a subclass
        of BaseModel.
        If validation errors are encountered, they are collected and returned.

        Args:
            loc (TLoc): The location context for the validation.
            field (str): The field name associated with the dictionary being validated.
            value (Dict[Any, Any]): The dictionary containing items to be validated.

        Returns:
            List[Error]: A list of validation errors encountered during the process.
        """
        errors = []
        for key, item in value.items():
            if issubclass(type(item), BaseModel):
                try:
                    self.validate_model(loc + [field, key], item)
                except ModelError as e:
                    errors.extend(e.errors)
        return errors

    def __validate_customs_model_basemodel(self, loc: TLoc, field: str, value: BaseModel) -> List[Error]:
        """
        Validates a custom model that inherits from BaseModel.

        Args:
            loc (TLoc): The location of the field being validated.
            field (str): The name of the field being validated.
            value (BaseModel): The model instance to validate.

        Returns:
            List[Error]: A list of validation errors, if any.
        """
        errors = []
        try:
            self.validate_model(loc + [field], value)
        except ModelError as e:
            errors.extend(e.errors)
        return errors

    def __validate_customs_model_fields(self, loc: TLoc, model: BaseModel) -> List[Error]:
        """
        Validates the fields of a custom model and returns a list of errors.

        Args:
            loc (TLoc): The location context for the validation.
            model (BaseModel): The model instance to be validated.

        Returns:
            List[Error]: A list of errors found during validation.

        Raises:
            ValidationError: If the model validation fails.
        """
        errors = []
        try:
            model.model_validate(model.__dict__)
        except ValidationError as e:
            for error in e.errors():
                if error['input'] is None and model.model_fields[error['loc'][0]].is_required():
                    error['msg'] = 'Field required'
                    error['type'] = 'missing'
                errors.append(Error(type=error['type'], msg=error['msg'], loc=loc + list(error['loc'])))
        return errors
