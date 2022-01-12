from app.Context import Context
from app.Resource import Resource, Action
from app.errors.InvalidArgumentError import InvalidArgumentError
from database.dataclasses.Pattern import Pattern


class Patterns(Resource):

    def __init__(self):
        """
        Constructor.
        """
        super().__init__()

        # Methods
        self._method("create", Action.CREATE, self.create)
        self._method("delete", Action.DELETE, self.delete)
        self._method("get", Action.GET, self.get)
        self._method("list", Action.GET, self.list)
        self._method("set", Action.CREATE, self.set)

    @staticmethod
    def create(context: Context, pattern_id: str) -> Pattern:
        """
        Create a pattern.

        :param context: The context.
        :param pattern_id: Identifier of the pattern.
        :return: The newly created pattern.
        """
        pattern = Pattern(identifier=pattern_id)
        context.database.add_pattern(pattern)
        return pattern

    @staticmethod
    def delete(context: Context, pattern_id: str) -> None:
        """
        Delete a pattern.

        :param context: The context.
        :param pattern_id: Identifier of the pattern.
        """
        context.database.remove_pattern(pattern_id)

    @staticmethod
    def get(context: Context, pattern_id: str) -> Pattern:
        """
        Get a pattern.

        :param context: The context.
        :param pattern_id: Identifier of the pattern. An exception is raised if no pattern with this identifier is
         found.
        :return:The pattern having the given identifier.
        """
        return context.database.get_pattern(pattern_id)

    @staticmethod
    def list(context: Context) -> list[Pattern]:
        """
        Get the list of patterns.

        :param context: The context.
        :return: List of patterns sorted by identifier.
        """
        patterns = context.database.get_patterns()
        patterns.sort()
        return patterns

    @staticmethod
    def set(context: Context, pattern_id: str, role: str, number: str) -> None:
        """
        Set an assignment of a pattern.

        :param context: The context.
        :param pattern_id: Identifier of the pattern.
        :param role: Role to set.
        :param number: Number of persons required for the role.
        """
        try:
            if not role:
                raise InvalidArgumentError("role")

            if int(number) <= 0:
                raise InvalidArgumentError("number")

            pattern = context.database.get_pattern(pattern_id)
            pattern.assignments[role] = int(number)
        except ValueError:
            raise InvalidArgumentError("number")
