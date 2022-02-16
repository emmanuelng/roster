from app.Context import Context
from app.Resource import Resource, Action
from app.resources.PersonAbsences import PersonAbsences
from app.resources.PersonRoles import PersonRoles
from database.dataclass.Person import Person


class Persons(Resource):

    def __init__(self) -> None:
        """
        Constructor.
        """
        super().__init__()

        # Child resources
        self._child_resource("roles", PersonRoles())
        self._child_resource("absences", PersonAbsences())

        # Methods
        self._method("create", Action.CREATE, self.create)
        self._method("get", Action.GET, self.get)
        self._method("list", Action.GET, self.list)

    @staticmethod
    def create(context: Context, identifier: str, first_name: str, last_name: str) -> Person:
        """
        Create a person.
        
        :param context: The context.
        :param identifier: Identifier of the new person. An exception is raised if another person with the same
         identifier exists.
        :param first_name: First name of the new person.
        :param last_name: Last name of the new person.
        :return: The newly created person.
        """
        return context.database.create(Person, identifier=identifier, first_name=first_name, last_name=last_name)

    @staticmethod
    def delete(context: Context, identifier: str) -> None:
        """
        Delete a person.

        :param context: The context.
        :param identifier: Identifier of the person.
        """
        context.database.delete(Person, identifier=identifier)

    @staticmethod
    def get(context: Context, person_id: str) -> Person:
        """
        Get a person.

        :param context: The context.
        :param person_id: Identifier of the person. An exception is raised if no person with this identifier is found.
        :return: The person with the given identifier.
        """
        return context.database.get_unique(Person, identifier=person_id)

    @staticmethod
    def list(context: Context) -> list[Person]:
        """
        Get the list of persons.

        :param context: The context.
        :return: The list of all registered persons, sorted by last name / first name.
        """
        persons: list[Person] = context.database.get(Person)
        persons.sort(key=lambda p: f"{p.last_name, p.first_name}")
        return persons
