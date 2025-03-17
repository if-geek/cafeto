import inspect
from typing import Callable

from cafeto.models.base_model import BaseModel
from cafeto.mvc.base_controller import BaseController
from cafeto.mvc.types import Action
from cafeto.responses import Response


class OnBeforeAction:
    """
    Singleton class to manage and execute subscriptions before an action is performed.
    This class ensures that only one instance of itself is created and provides methods
    to add, remove, clear, and execute subscription functions.

    Attributes:
        __instance (OnAfterAction): The singleton instance of the class.
        subscriptions (list): A list of subscribed functions to be executed after an action.
    """
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
            cls.__instance.subscriptions = []
        return cls.__instance

    @staticmethod
    def add(func: Callable):
        """
        Adds a function to the list of subscriptions for the OnBeforeAction event.

        Args:
            func (Callable): The function to be added to the subscriptions list.
        """
        if OnBeforeAction.__instance is None:
            OnBeforeAction.__instance = OnBeforeAction()
        OnBeforeAction.__instance.subscriptions.append(func)

    @staticmethod
    def remove(func: Callable):  # pragma: no cover
        """
        Remove a function from the list of subscriptions.

        Args:
            func (Callable): The function to be removed from the subscriptions list.
        """
        if OnBeforeAction.__instance is not None:
            OnBeforeAction.__instance.subscriptions.remove(func)

    @staticmethod
    def clear():  # pragma: no cover
        """
        Clears all subscriptions from the OnBeforeAction instance.

        This method checks if the OnBeforeAction instance is not None,
        and if so, clears all subscriptions associated with it.
        """
        if OnBeforeAction.__instance is not None:
            OnBeforeAction.__instance.subscriptions.clear()

    @staticmethod
    async def execute(controller: BaseController, action: Action):
        """
        Executes the given action on the specified controller, invoking any subscribed
        functions before the action is executed.

        Args:
            controller (BaseController): The controller on which the action is to be executed.
            action (Action): The action to be executed.
        """
        if OnBeforeAction.__instance is not None:
            for func in OnBeforeAction.__instance.subscriptions:
                if inspect.iscoroutinefunction(func):  # pragma: no cover
                    await func(controller, action)
                else:
                    func(controller, action)


class OnExecuteAction:
    """
    Singleton class to manage and execute subscribed actions.
    This class ensures that only one instance exists and provides methods to add, remove, clear,
    and execute subscribed functions.

    Attributes:
        __instance (OnAfterAction): The singleton instance of the class.
        subscriptions (list): A list of subscribed functions to be executed after an action.
    """
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
            cls.__instance.subscriptions = []
        return cls.__instance

    @staticmethod
    def add(func: Callable):
        """
        Adds a function to the list of subscriptions for the OnExecuteAction event.

        Args:
            func (Callable): The function to be added to the subscriptions list.
        """
        if OnExecuteAction.__instance is None:
            OnExecuteAction.__instance = OnExecuteAction()
        OnExecuteAction.__instance.subscriptions.append(func)

    @staticmethod
    def remove(func: Callable):  # pragma: no cover
        """
        Removes a function from the list of subscriptions if an instance of OnExecuteAction exists.

        Args:
            func (Callable): The function to be removed from the subscriptions list.
        """
        if OnExecuteAction.__instance is not None:
            OnExecuteAction.__instance.subscriptions.remove(func)

    @staticmethod
    def clear():  # pragma: no cover
        """
        Clears all subscriptions from the OnExecuteAction instance.

        This method checks if the OnExecuteAction instance is not None and
        then clears its subscriptions list.
        """
        if OnExecuteAction.__instance is not None:
            OnExecuteAction.__instance.subscriptions.clear()

    @staticmethod
    async def execute(controller: BaseController, action: Action, request_model: BaseModel):
        """
        Executes the given action on the controller with the provided request model.

        This method iterates over all subscribed functions in the OnExecuteAction instance
        and calls them with the provided controller, action, and request model. If a
        subscribed function is a coroutine, it is awaited.

        Args:
            controller (BaseController): The controller on which the action is executed.
            action (Action): The action to be executed.
            request_model (BaseModel): The request model containing the data for the action.
        """
        if OnExecuteAction.__instance is not None:
            for func in OnExecuteAction.__instance.subscriptions:
                if inspect.iscoroutinefunction(func):  # pragma: no cover
                    await func(controller, action, request_model)
                else:
                    func(controller, action, request_model)


class OnAfterAction:
    """
    Singleton class to manage and execute subscriptions after an action.
    This class ensures that only one instance exists and provides methods to add, remove, clear, and execute
    subscribed functions.

    Attributes:
        __instance (OnAfterAction): The singleton instance of the class.
        subscriptions (list): A list of subscribed functions to be executed after an action.
    """
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
            cls.__instance.subscriptions = []
        return cls.__instance

    @staticmethod
    def add(func: Callable):
        """
        Adds a function to the list of subscriptions for the OnAfterAction event.

        Args:
            func (Callable): The function to be added to the subscriptions list.
        """
        if OnAfterAction.__instance is None:
            OnAfterAction.__instance = OnAfterAction()
        OnAfterAction.__instance.subscriptions.append(func)

    @staticmethod
    def remove(func: Callable):  # pragma: no cover
        """
        Removes a function from the list of subscriptions.

        Args:
            func (Callable): The function to be removed from the subscriptions.
        """
        if OnAfterAction.__instance is not None:
            OnAfterAction.__instance.subscriptions.remove(func)

    @staticmethod
    def clear():  # pragma: no cover
        """
        Clears all subscriptions from the OnAfterAction instance.

        This method removes all the subscriptions from the OnAfterAction singleton instance,
        effectively resetting its state. This method is not covered by tests as indicated
        by the pragma directive.
        """
        if OnAfterAction.__instance is not None:
            OnAfterAction.__instance.subscriptions.clear()

    @staticmethod
    async def execute(controller: BaseController, action: Action, request_model: BaseModel, response: Response):
        """
        Executes the given action on the controller and triggers any subscribed functions after the action.

        Args:
            controller (BaseController): The controller on which the action is executed.
            action (Action): The action to be executed.
            request_model (BaseModel): The request model containing the data for the action.
            response (Response): The response object to be populated by the action.
        """
        if OnAfterAction.__instance is not None:
            for func in OnAfterAction.__instance.subscriptions:
                if inspect.iscoroutinefunction(func):  # pragma: no cover
                    await func(controller, action, request_model, response)
                else:
                    func(controller, action, request_model, response)
