from database.Database import Database
from database.dataclass.Person import Person
from database.dataclass.Roster import Roster
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
        all_rosters = self.__database.get(Roster)
        past_rosters = filter(lambda r: r.sequence_no < roster_sequence_no, all_rosters)
        sorted_rosters = sorted(past_rosters, key=lambda r: r.sequence_no, reverse=True)

        for i, roster in enumerate(sorted_rosters):
            if roster.is_assigned(person, role):
                return 1.0 - (1.0 / (i + 1))

        return 1.0
