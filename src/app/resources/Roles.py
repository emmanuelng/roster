from app.Context import Context
from app.Resource import Resource, Action
from database.dataclass.Pattern import Pattern
from database.dataclass.Person import Person


class Roles(Resource):

    def __init__(self):
        """
        Constructor.
        """
        super().__init__()

        # Methods
        self._method("get", Action.GET, self.get)

    @staticmethod
    def get(context: Context) -> list[str]:
        """
        Get the list of all roles.

        :param context: The context.
        :return: A sorted list of roles.
        """
        all_patterns: list[Pattern] = context.database.get(Pattern)
        all_persons: list[Person] = context.database.get(Person)

        roles = [pattern.roles for pattern in all_patterns] + [person.roles for person in all_persons]
        roles = list(set([item for sublist in roles for item in sublist]))
        roles.sort()

        return roles
