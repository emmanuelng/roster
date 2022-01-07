from app.Context import Context
from app.Resource import Resource, Action
from app.errors.InvalidArgumentError import InvalidArgumentError
from app.resources.PersonAbsences import PersonAbsences
from app.resources.Roles import Roles
from dataset.dataclasses.Person import Person


class Persons(Resource):

    def __init__(self) -> None:
        super().__init__()

        # Child resources
        self._child_resource("roles", Roles())
        self._child_resource("absences", PersonAbsences())

        # Methods
        self._method("create", Action.CREATE, self.create)
        self._method("get", Action.GET, self.get)
        self._method("list", Action.GET, self.list)

    @staticmethod
    def create(context: Context, identifier: str, first_name: str, last_name: str) -> None:
        """
        Create a new person.
        """
        person = Person(identifier, first_name, last_name)
        context.dataset.add_person(person)

    @staticmethod
    def delete(context: Context, identifier: str) -> None:
        """
        Delete a person.
        """
        context.dataset.remove_person(identifier)

    @staticmethod
    def get(context: Context, person_id: str) -> Person:
        """
        Get a specific persons.
        """
        if person_id is None:
            raise InvalidArgumentError("person_id")

        return context.dataset.get_person(person_id)

    @staticmethod
    def list(context: Context) -> list[Person]:
        """
        Get the list of persons.
        """
        return context.dataset.get_persons()
