from app.Context import Context
from app.Resource import Resource
from dataset.dataclasses.Pattern import Pattern


class Patterns(Resource):

    @staticmethod
    def create(context: Context, pattern_id: str) -> None:
        """
        Create a new pattern.
        """
        context.dataset.add_pattern(Pattern(pattern_id))

    @staticmethod
    def delete(context: Context, pattern_id: str) -> None:
        """
        Delete a pattern.
        """
        context.dataset.remove_pattern(pattern_id)

    @staticmethod
    def get(context: Context, pattern_id: str) -> Pattern:
        """
        Display the details of a pattern.
        """
        return context.dataset.get_pattern(pattern_id)

    @staticmethod
    def list(context: Context) -> list[Pattern]:
        """
        Display the list of patterns.
        """
        return context.dataset.get_patterns()

    @staticmethod
    def set(context: Context, pattern_id: str, role: str, number: str) -> None:
        """
        Set an assignment of a pattern.
        """
        pattern = context.dataset.get_pattern(pattern_id)
        pattern.assignments[role] = int(number)
