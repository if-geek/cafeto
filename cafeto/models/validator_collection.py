from typing import Dict, Callable

from pydantic import BaseModel


class ClassProperty:
    def __init__(self, getter):
        self.getter = getter

    def __get__(self, _, owner):
        return self.getter(owner)


class ValidatorCollection:
    """
    A singleton class that manages a collection of validation functions for different models.
    Attributes:
        instance (ValidatorCollection): The singleton instance of the class.
        __validations (Dict[str, Dict[str, str]]): A dictionary storing validation functions for each model.
    Methods:
        validations() -> Dict[str, Dict[str, str]]:
            Class property that returns the dictionary of validations.
        add_validation(field: str, func: Callable):
            Adds a validation function for a specific field of a model.
        set_parent_validations(cls_base: BaseModel):
            Sets the parent validations for a given model class.
        get_validation(model_name: str) -> Dict[str, str]:
            Returns the validation functions for a specific model.
        clear():
            Clears all the validations.
    """
    instance: 'ValidatorCollection' = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(ValidatorCollection, cls).__new__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self):
        self.__validations: Dict[str, Dict[str, str]] = {}

    @ClassProperty
    def validations(cls) -> Dict[str, Dict[str, str]]:  # noqa
        return cls.instance.__validations

    @classmethod
    def add_validation(cls, field, func: Callable):
        model_name, method_name = func.__qualname__.split('.')
        full_model_name = f"{func.__module__}.{model_name}"
        if full_model_name in cls.validations:
            cls.validations[full_model_name][field] = method_name
        else:
            cls.validations[full_model_name] = {field: method_name}

    @classmethod
    def set_parent_validations(cls, cls_base: BaseModel):
        for base in cls_base.__mro__:
            base_full_model_name = f"{base.__module__}.{base.__name__}"
            if base_full_model_name in cls.validations:
                current_model_name = f"{cls_base.__module__}.{cls_base.__name__}"
                if current_model_name not in cls.validations:
                    cls.validations[current_model_name] = {}
                cls.validations[current_model_name].update(cls.validations[base_full_model_name])

    @classmethod
    def get_validation(cls, model_name: str) -> Dict[str, str]:  # pragma: no cover
        return cls.validations.get(model_name)

    @classmethod
    def clear(cls):  # pragma: no cover
        cls.validations.clear()


ValidatorCollection()
