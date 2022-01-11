from abc import ABC, abstractmethod

from app.Context import Context
from app.Resource import Resource
from app.errors.MethodNotFoundError import MethodNotFoundError
from app.resources.Configurations import Configurations
from app.resources.Patterns import Patterns
from app.resources.Persons import Persons
from app.resources.Roles import Roles
from app.resources.Rosters import Rosters
from database.Database import Database


class App(ABC):
    """
    Application class.
    """

    __context: Context
    __resources: dict[str, Resource]

    def __init__(self, database: Database) -> None:
        """
        Constructor.

        :param database: Database used by the application.
        """
        self.__context = Context(database)
        self.__resources = {}

        # Resources
        self._resource("config", Configurations())
        self._resource("patterns", Patterns())
        self._resource("persons", Persons())
        self._resource("roles", Roles())
        self._resource("rosters", Rosters())

    def execute_method(self, path: list[str], *args) -> any:
        """
        Finds and executes a method from a resource.

        :param path: Path of the method (e.g. ['person', 'role', 'add']).
        :param args: List of arguments.
        :return: The result of the method.
        """
        if len(path) > 1:
            resource = self.__resources.get(path[0], None)
            if resource is not None:
                context = self.__context
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
        self.__resources[name] = resource
