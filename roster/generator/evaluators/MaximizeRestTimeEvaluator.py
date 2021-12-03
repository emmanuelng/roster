from dataset.Dataset import Dataset
from dataset.objects.Person import Person
from generator.Evaluator import Evaluator


class MaximizeRestTimeEvaluator(Evaluator):

    def __init__(self, dataset: Dataset) -> None:
        self._dataset = dataset

    def assignment_score(self, roster_sequence_no: int, person: Person, role: str) -> float:
        past_rosters = self._dataset.get_rosters(before=roster_sequence_no)
        sorted_rosters = sorted(past_rosters, key=lambda r: r.sequence_no, reverse=True)

        for i, roster in enumerate(sorted_rosters):
            if roster.is_assigned(person):
                return 1.0 - (1.0 / (i + 1))

        return 1.0
