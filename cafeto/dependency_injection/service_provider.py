
from typing import Dict, Optional, Type
from types import FunctionType
from contextvars import ContextVar, Token

from cafeto.dependency_injection.service_collection import ServiceCollection, ServiceData


# ContextVar to store a copy of the scoped dependencies
# This is used to resolve dependencies within the scope of a request
# without affecting the original scoped dependencies
scoped_copy_var: ContextVar[dict] = ContextVar("scoped_copy")


class ServiceProvider:
    """
    A class to manage dependency injection for different lifetimes: singleton, transient, and scoped.

    Attributes:
        singleton (Dependencies): A dictionary to store singleton dependencies.
        transient (Dependencies): A dictionary to store transient dependencies.
        scoped (Dependencies): A dictionary to store scoped dependencies.
    """

    instance: 'ServiceProvider' = None

    def __new__(cls, *args, **kwargs):
        """
        Create a new instance of the class if it doesn't already exist.

        This method overrides the default behavior of the __new__ method to implement
        the singleton pattern. It ensures that only one instance of the class is created.

        Args:
            cls: The class being instantiated.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The single instance of the class.
        """
        if not cls.instance:
            cls.instance = super(ServiceProvider, cls).__new__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self):
        ServiceCollection()

    @classmethod
    def scoped_copy(cls) -> Token:
        """
        Creates a scoped copy of the service collection and sets it to a scoped variable.

        This method is necessary to ensure that each scope has its own instance of the service collection,
        which helps in managing the lifecycle of services and their dependencies within that scope.
        By creating a scoped copy, we can isolate the services used in different scopes, preventing
        unintended interactions and ensuring that each scope has a clean and independent set of services.

        Returns:
            Token: A token representing the scoped variable containing the copied service collection.
        """
        scoped_copy = ServiceCollection.copy_scoped()
        scoped_copy_var_token = scoped_copy_var.set(scoped_copy)
        return scoped_copy_var_token

    @classmethod
    def resolve(cls, obj: Type | FunctionType) -> Dict[str, object]:
        """
        Resolves the dependencies for the given object type or function.

        Args:
            obj (Type | FunctionType): The object type or function for which dependencies need to be resolved.

        Returns:
            Dict[str, object]: A dictionary containing the resolved dependencies.
        """
        return cls.instance.__resolve_dependency(obj)

    def __resolve_dependency(self, obj: Type | FunctionType) -> Dict[str, object]:
        """
        Resolves the dependencies for the given object type or function.
        This method inspects the annotations of the given object's `__init__` method
        or the function's annotations to determine the required dependencies. It then
        resolves each dependency and returns a dictionary mapping argument names to
        their resolved dependency instances.

        Args:
            obj (Type | FunctionType): The object type or function for which dependencies
                need to be resolved.

        Returns:
            Dict[str, object]: A dictionary where the keys are argument names and the values
                are the resolved dependency instances.
        """
        if '__init__' in obj.__dict__:
            annotations = obj.__init__.__annotations__
        else:
            annotations = obj.__annotations__

        dependencies: Dict[str, object] = {}

        for arg_name, dep_type in annotations.items():
            if arg_name == 'return':
                continue

            dependency = self.__resolve_single_dependency(dep_type)
            if dependency is not None:
                dependencies[arg_name] = dependency

        return dependencies

    def __resolve_single_dependency(self, dep_type: Type) -> Optional[object]:
        """
        Resolves a single dependency based on its type.
        This method checks if the dependency type is registered as a singleton, scoped, or transient
        and returns the corresponding instance. If the dependency type is not found in any of these
        categories, it returns None.

        Args:
            dep_type (Type): The type of the dependency to resolve.

        Returns:
            object: The resolved dependency instance or None if the dependency type is not registered.
        """
        scoped = scoped_copy_var.get()

        if dep_type in ServiceCollection.singleton:
            return self.__get_singleton_instance(dep_type)
        elif dep_type in scoped:
            return self.__get_scoped_instance(dep_type)
        elif dep_type in ServiceCollection.transient:
            return self.__get_transient_instance(dep_type)
        else:
            return None

    def __get_singleton_instance(self, dep_type: Type) -> object:
        """
        Retrieve a singleton instance of the specified dependency type.

        This method fetches the singleton instance from the ServiceCollection,
        resolves its dependencies, and sets its value if not already set.

        Args:
            dep_type (Type): The type of the dependency to retrieve.

        Returns:
            object: The singleton instance of the specified dependency type.
        """
        service_data: ServiceData = ServiceCollection.singleton[dep_type]
        service_data.set_value(**self.__resolve_dependency(service_data.dep_type))
        return service_data.value

    def __get_scoped_instance(self, dep_type: Type) -> object:
        """
        Retrieve a scoped instance of the specified dependency type.

        This method fetches the scoped instance of the given dependency type from
        the scoped copy variable. It resolves the dependency and sets its value
        before returning it.

        The `scoped_copy_var` is used to maintain a separate instance of dependencies
        for each scope, ensuring that dependencies are not shared across different
        scopes. This is particularly useful in scenarios such as web requests, where
        each request should have its own set of dependencies.

        Args:
            dep_type (Type): The type of the dependency to retrieve.

        Returns:
            object: The resolved instance of the specified dependency type.
        """
        scoped = scoped_copy_var.get()
        service_data: ServiceData = scoped[dep_type]
        service_data.set_value(**self.__resolve_dependency(service_data.dep_type))
        return service_data.value

    def __get_transient_instance(self, dep_type: Type) -> object:
        """
        Retrieves an instance of a transient service.

        Args:
            dep_type (Type): The type of the dependency to resolve.

        Returns:
            object: An instance of the requested transient service.
        """
        service_data: ServiceData = ServiceCollection.transient[dep_type]
        instance = service_data.get_instance(**self.__resolve_dependency(service_data.dep_type))
        return instance

    @classmethod
    def reset_scoped(cls, token: Token) -> None:
        """
        Resets the scoped variable associated with the given token.

        This method uses the `reset` method of the `ContextVar` class to reset the
        value of the scoped variable. The `ContextVar` class requires a token to
        reset the variable to its previous state. The token is obtained when the
        variable's value is set or modified, ensuring that the reset operation
        correctly restores the variable's state.

        Args:
            token (Token): The token associated with the scoped variable to reset.

        Returns:
            None
        """
        return scoped_copy_var.reset(token)
