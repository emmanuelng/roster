from abc import ABC, abstractmethod

from app.Context import Context
from app.Resource import Resource
from app.errors.MethodNotFoundError import MethodNotFoundError
from app.resources.Persons import Persons
from app.resources.Rosters import Rosters
from dataset.Dataset import Dataset


class App(ABC):
    """
    Application class.
    """

    _context: Context
    _resources: dict[str, Resource]

    def __init__(self, dataset: Dataset) -> None:
        """
        Constructor.

        :param dataset: Dataset used by the application.
        """
        self._context = Context(dataset)
        self._resources = {}

        # Resources
        self._resource("persons", Persons())
        self._resource("rosters", Rosters())

    def execute_method(self, path: list[str], *args) -> any:
        """
        Finds and executes a method from a resource.

        :param path: Path of the method (e.g. ['person', 'role', 'add']).
        :param args: List of arguments.
        :return: The result of the method.
        """
        if len(path) > 1:
            resource = self._resources.get(path[0], None)
            if resource is not None:
                context = self._context
                return resource.execute_method(path[1:], context, *args)

        raise MethodNotFoundError()

    @abstractmethod
    def start(self) -> None:
        """
        Starts the application.
        """
        pass

    def _resource(self, name: str, resource: Resource) -> None:
        """
        Adds a new resource.

        :param resource: Resource to add.
        """
        self._resources[name] = resource
