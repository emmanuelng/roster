from database.Database import Database
from database.dataclasses.Person import Person
from generator.Evaluator import Evaluator


class AlternateRolesEvaluator(Evaluator):
    """
    Helps to optimize the variety of roles assigned to a person. Returns a score close to zero if the person was
    assigned to the role recently.
    """

    __database: Database

    def __init__(self, database: Database) -> None:
        """
        Constructor.

        :param database: The database.
        """
        self.__database = database

    def assignment_score(self, roster_sequence_no: int, person: Person, role: str) -> float:
        past_rosters = self.__database.get_rosters(before=roster_sequence_no)
        sorted_rosters = sorted(past_rosters, key=lambda r: r.sequence_no, reverse=True)

        for i, roster in enumerate(sorted_rosters):
            if roster.is_assigned(person, role):
                return 1.0 - (1.0 / (i + 1))

        return 1.0
