from __future__ import annotations

from abc import ABC
from collections import Callable
from dataclasses import dataclass
from enum import Enum, auto

from app.errors.MethodNotFoundError import MethodNotFoundError


class Resource(ABC):
    """
    Class representing a resource of an application. Resources can be viewed as groups of methods. They can have
    sub-resources.
    """

    _methods: dict[str, Method]
    _child_resources: dict[str, Resource]

    def __init__(self):
        """
        Constructor.
        """
        self._methods = {}
        self._child_resources = {}

    @property
    def children(self) -> list[Resource]:
        """
        Child resources.
        """
        return self._child_resources.values()

    @property
    def methods(self) -> list[Method]:
        """
        Resource methods.
        """
        return self._methods.values()

    def execute_method(self, path: list[str], *args) -> any:
        """
        Finds and executes a method.

        :param path: Path of the method.
        :param args: Arguments.
        :return: Result of the method.
        """
        path_size = len(path)

        # The path contains one element: call the corresponding method.
        if path_size == 1:
            method = self._methods.get(path[0], None)
            if method is not None:
                return method(*args)

        # The path contains multiple elements: go to the next child resource.
        elif path_size > 1:
            child = self._child_resources.get(path[0], None)
            if child is not None:
                return child.execute_method(path[1:], *args)

        raise MethodNotFoundError()

    def _child_resource(self, name: str, resource: Resource) -> None:
        """
        Adds a sub-resource.

        :param name: Name of the child resource.
        :param resource: Child resource.
        """
        self._child_resources[name] = resource

    def _method(self, name: str, action: Action, func: Callable) -> None:
        """
        Adds a method.

        :param name: Name of the method.
        :param action: Type of action performed by the method.
        :param func: Method function.
        """
        self._methods[name] = Method(name, action, func)


class Action(Enum):
    """
    Represents the actions performed by the methods.
    """

    GET = auto()
    CREATE = auto()
    UPDATE = auto()
    DELETE = auto()


@dataclass(frozen=True)
class Method:
    """
    Class representing a method of a resource.
    """

    name: str
    action: Action
    func: Callable

    def __call__(self, *args, **kwargs) -> any:
        return self.func(*args, **kwargs)