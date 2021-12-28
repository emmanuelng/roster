from dataset.Dataset import Dataset
from dataset.dataclasses.Person import Person
from generator.Evaluator import Evaluator


class AlternateRolesEvaluator(Evaluator):
    """
    Helps to optimize the variety of roles assigned to a person. Returns a score close to zero if the person was
    assigned to the role recently.
    """

    def __init__(self, dataset: Dataset) -> None:
        """
        Constructor.

        :param dataset: The dataset.
        """
        self._dataset = dataset

    def assignment_score(self, roster_sequence_no: int, person: Person, role: str) -> float:
        past_rosters = self._dataset.get_rosters(before=roster_sequence_no)
        sorted_rosters = sorted(past_rosters, key=lambda r: r.sequence_no, reverse=True)

        for i, roster in enumerate(sorted_rosters):
            if roster.is_assigned(person, role):
                return 1.0 - (1.0 / (i + 1))

        return 1.0
