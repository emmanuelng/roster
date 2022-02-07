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
        roles = [pattern.roles for pattern in context.database.get(Pattern)] + \
                [person.roles for person in context.database.get(Person)]

        roles = list(set([item for sublist in roles for item in sublist]))
        roles.sort()

        return roles
