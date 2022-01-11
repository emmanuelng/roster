from app.Context import Context
from app.Resource import Resource, Action


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
        roles = []

        for pattern in context.database.get_patterns():
            roles += pattern.roles

        for person in context.database.get_persons():
            roles += person.roles

        roles = list(set(roles))
        roles.sort()

        return roles
