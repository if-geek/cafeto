from typing import Callable, Dict, Literal, Optional, Type, overload


class ClassProperty:
    def __init__(self, getter):
        self.getter = getter

    def __get__(self, _, owner):
        return self.getter(owner)


class ServiceData:
    """
    A class to represent a service data for dependency injection.

    Attributes:
        type (Literal['singleton', 'transient', 'scoped']): The lifecycle type of the service.
        dep_type (Type): The type of the dependency.
        implementation (Type): The implementation type of the service.
        generator (Optional[Callable], optional): A callable to generate the service instance, by default None.
        value (Type): The cached instance of the service, used for singleton and scoped lifecycles.
    """
    def __init__(
            self,
            type: Literal['singleton', 'transient', 'scoped'],
            dep_type: Type,
            implementation: Type,
            generator: Optional[Callable] = None
            ):
        self.type: Literal['singleton', 'transient', 'scoped'] = type
        self.dep_type: Type = dep_type
        self.implementation: Type = implementation
        self.generator: Callable = generator
        self.value: Type = None

    def set_value(self, **params) -> None:
        """
        Sets the value of the service instance if it is not already set and the service type is not 'transient'.

        Args:
            **params: Arbitrary keyword arguments that are passed to the get_instance method to create the service
            instance.

        Returns:
            None
        """
        if self.type == 'transient' or self.value is not None:
            return

        self.value = self.get_instance(**params)

    def get_instance(self, **params) -> Type:
        """
        Creates and returns an instance of the implementation class.
        If a generator function is provided, it will be used to create the instance.
        Otherwise, it checks if the constructor of the dependency type has annotations.
        If annotations are present, the instance is created with the provided parameters.
        If no annotations are present, the instance is created without parameters.

        Args:
            **params: Arbitrary keyword arguments to pass to the constructor of the implementation.

        Returns:
            Type: An instance of the implementation class.
        """
        if self.generator is not None:
            return self.generator(**params)

        if getattr(self.dep_type.__init__, '__annotations__', None):
            instance = self.implementation(**params)
        else:
            instance = self.implementation()

        return instance

    def copy(self) -> 'ServiceData':
        """
        Creates a copy of the current ServiceData instance.

        Returns:
            ServiceData: A new instance of ServiceData with the same type, dependency type,
                         implementation, and generator as the current instance.
        """
        return ServiceData(self.type, self.dep_type, self.implementation, self.generator)


Dependencies = Dict[Type, ServiceData]


class ServiceCollection:
    """
    A class to manage dependency injection for different lifetimes: singleton, transient, and scoped.

    Attributes:
        singleton (Dependencies): A dictionary to store singleton dependencies.
        transient (Dependencies): A dictionary to store transient dependencies.
        scoped (Dependencies): A dictionary to store scoped dependencies.
    """
    instance: 'ServiceCollection' = None

    def __new__(cls, *args, **kwargs):
        """
        Create a new instance of the class if it doesn't already exist.

        This method ensures that only one instance of the class is created (singleton pattern).
        If an instance already exists, it returns the existing instance.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            ServiceCollection: The single instance of the ServiceCollection class.
        """
        if not cls.instance:
            cls.instance = super(ServiceCollection, cls).__new__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self):
        self.__singleton: Dependencies = {}
        self.__scoped: Dependencies = {}
        self.__transient: Dependencies = {}

    @ClassProperty
    def singleton(cls) -> Dependencies: # noqa
        """
        Gets the singleton dependencies.

        Returns:
            Dependencies: The singleton dependencies.
        """
        return cls.instance.__singleton

    @ClassProperty
    def scoped(cls) -> Dependencies: # noqa
        """
        Gets the scoped dependencies.

        Returns:
            Dependencies: The scoped dependencies.
        """
        return cls.instance.__scoped

    @ClassProperty
    def transient(cls) -> Dependencies: # noqa
        """
        Gets the transient dependencies.

        Returns:
            Dependencies: The transient dependencies.
        """
        return cls.instance.__transient

    @overload
    @classmethod
    def add_singleton(cls, implementation: Type, *, override: bool = False):  # pragma: no cover
        ...

    @overload
    @classmethod
    def add_singleton(cls, dep_type: Type, implementation: Type, *, override: bool = False):  # pragma: no cover
        ...

    @overload
    @classmethod
    def add_singleton(cls, implementation: Type, generator: Callable, *, override: bool = False):  # pragma: no cover
        ...

    @overload
    @classmethod
    def add_singleton(
        cls,
        dep_type: Type,
        implementation: Type,
        generator: Callable,
        *,
        override: bool = False
    ):  # pragma: no cover
        ...

    @classmethod
    def add_singleton(
        cls,
        dep_type: Type,
        implementation: Optional[Type] = None,
        generator: Callable = None,
        *,
        override: bool = False
    ) -> None:
        """
        Registers a singleton service in the service collection.

        Args:
            dep_type (Type): The type of the service to register.
            implementation (Optional[Type], optional): The implementation type of the service. Defaults to None.
            generator (Callable, optional): A callable that generates the service instance. Defaults to None.

        Returns:
            None
        """
        cls.__add_service(cls.singleton, 'singleton', dep_type, implementation, generator, override)

    @classmethod
    def remove_singleton(cls, dep_type: Type) -> None:
        """
        Removes a singleton service from the service collection.

        Args:
            dep_type (Type): The type of the service to remove.
        """
        if dep_type in cls.singleton:
            del cls.singleton[dep_type]

    @overload
    @classmethod
    def add_scoped(cls, implementation: Type, *, override: bool = False):  # pragma: no cover
        ...

    @overload
    @classmethod
    def add_scoped(cls, dep_type: Type, implementation: Type, *, override: bool = False):  # pragma: no cover
        ...

    @overload
    @classmethod
    def add_scoped(cls, implementation: Type, generator: Callable, *, override: bool = False):  # pragma: no cover
        ...

    @overload
    @classmethod
    def add_scoped(
        cls,
        dep_type: Type,
        implementation: Type,
        generator: Callable,
        *,
        override: bool = False
    ):  # pragma: no cover
        ...

    @classmethod
    def add_scoped(
        cls,
        dep_type: Type,
        implementation: Optional[Type] = None,
        generator: Callable = None,
        *,
        override: bool = False
    ) -> None:
        """
        Registers a scoped service with the service collection.

        A scoped service is created once per request within the scope. It is disposed of at the end of the request.

        Args:
            dep_type (Type): The type of the service to register.
            implementation (Optional[Type], optional): The implementation type of the service. Defaults to None.
            generator (Callable, optional): A callable that generates the service instance. Defaults to None.

        Returns:
            None
        """
        cls.__add_service(cls.scoped, 'scoped', dep_type, implementation, generator, override)

    @classmethod
    def remove_scoped(cls, dep_type: Type) -> None:
        """
        Removes a scoped service from the service collection.

        Args:
            dep_type (Type): The type of the service to remove.
        """
        if dep_type in cls.scoped:
            del cls.scoped[dep_type]

    @overload
    @classmethod
    def add_transient(cls, implementation: Type, *, override: bool = False):  # pragma: no cover
        ...

    @overload
    @classmethod
    def add_transient(cls, dep_type: Type, implementation: Type, *, override: bool = False):  # pragma: no cover
        ...

    @overload
    @classmethod
    def add_transient(cls, implementation: Type, generator: Callable, *, override: bool = False):  # pragma: no cover
        ...

    @overload
    @classmethod
    def add_transient(
        cls,
        dep_type: Type,
        implementation: Type,
        generator: Callable,
        *,
        override: bool = False
    ):  # pragma: no cover
        ...

    @classmethod
    def add_transient(
        cls,
        dep_type: Type,
        implementation: Optional[Type] = None,
        generator: Callable = None,
        *,
        override: bool = False
    ) -> None:
        """
        Registers a transient service with the service collection.

        A transient service is created each time it is requested.

        Args:
            dep_type (Type): The type of the service to register.
            implementation (Optional[Type], optional): The implementation type of the service. Defaults to None.
            generator (Callable, optional): A callable that generates the service instance. Defaults to None.

        Returns:
            None
        """
        cls.__add_service(cls.transient, 'transient', dep_type, implementation, generator, override)

    @classmethod
    def remove_transient(cls, dep_type: Type) -> None:
        """
        Removes a transient service from the service collection.

        Args:
            dep_type (Type): The type of the service to remove.
        """
        if dep_type in cls.transient:
            del cls.transient[dep_type]

    @classmethod
    def __add_service(
        cls,
        service_db: Dependencies,
        type: Literal['singleton', 'transient', 'scoped'],
        dep_type: Type,
        implementation: Optional[Type] = None,
        generator: Callable = None,
        override: bool = False
    ) -> None:
        """
        Adds a service to the service database.

        Args:
            cls: The class to which this method belongs.
            service_db (Dependencies): The service database where the service will be added.
            type (str): The name of the service to be added.
            dep_type (Type): The type of the dependency.
            implementation (Optional[Type], optional): The implementation type of the service. Defaults to None.
            generator (Callable, optional): A callable that generates the service instance. Defaults to None.

        Returns:
            None
        """

        if dep_type in service_db and not override:  # pragma: no cover
            return

        if generator is not None:
            service_db[dep_type] = ServiceData(type, dep_type, implementation or dep_type, generator)
        else:
            service_db[dep_type] = ServiceData(type, dep_type, implementation or dep_type, None)

    @classmethod
    def clear(cls) -> None:
        """
        Clears the collection of all dependencies.
        """
        cls.instance.__singleton.clear()
        cls.instance.__scoped.clear()
        cls.instance.__transient.clear()

    @classmethod
    def copy_scoped(cls) -> Dependencies:
        """
        Copies the scoped dependencies.

        Returns:
            Dependencies: A copy of the scoped dependencies.
        """
        copy = {}
        for dep_type, service_data in cls.instance.__scoped.items():
            copy[dep_type] = service_data.copy()
        return copy
