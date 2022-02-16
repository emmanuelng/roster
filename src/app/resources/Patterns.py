from typing import Union

from app.Context import Context
from app.Resource import Resource, Action
from app.errors.InvalidArgumentError import InvalidArgumentError
from database.dataclass.Pattern import Pattern


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
        return context.database.create(Pattern, identifier=pattern_id)

    @staticmethod
    def delete(context: Context, pattern_id: str) -> None:
        """
        Delete a pattern.

        :param context: The context.
        :param pattern_id: Identifier of the pattern.
        """
        context.database.delete(Pattern, identifier=pattern_id)

    @staticmethod
    def get(context: Context, pattern_id: str) -> Pattern:
        """
        Get a pattern.

        :param context: The context.
        :param pattern_id: Identifier of the pattern. An exception is raised if no pattern with this identifier is
         found.
        :return:The pattern having the given identifier.
        """
        return context.database.get_unique(Pattern, identifier=pattern_id)

    @staticmethod
    def list(context: Context) -> list[Pattern]:
        """
        Get the list of patterns.

        :param context: The context.
        :return: List of patterns sorted by identifier.
        """
        patterns: list[Pattern] = context.database.get(Pattern)
        patterns.sort(key=lambda p: p.identifier)
        return patterns

    @staticmethod
    def set(context: Context, pattern_id: str, role: str, number: Union[int, str]) -> None:
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

            pattern: Pattern = context.database.get_unique(Pattern, identifier=pattern_id)
            assignments = pattern.assignments
            assignments[role] = int(number)
            context.database.update(pattern, assignments=assignments)
        except ValueError:
            raise InvalidArgumentError("number")
