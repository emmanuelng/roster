from abc import ABC, abstractmethod

from dataset.Dataset import Dataset
from dataset.objects.Person import Person
from dataset.objects.Roster import Roster
from generator import Generator


class Algorithm(ABC):

    def __init__(self, generator: Generator) -> None:
        self._generator = generator

    @property
    def dataset(self) -> Dataset:
        """
        Dataset used by this algorithm.
        """
        return self._generator.dataset

    def assignment_score(self, roster_sequence_no: int, person: Person, role: str) -> float:
        """
        Evaluates an assignment in a roster.

        :param roster_sequence_no: The sequence number of the roster.
        :param person: The person.
        :param role: The role of the person.
        :return: A score. The higher the score, the better the assignment.
        """
        total_weight = 0
        score = 0.0

        for name, evaluator in self._generator.evaluators.items():
            weight = int(self._generator.configuration.get("weight_" + name, 1))
            score += (evaluator.assignment_score(roster_sequence_no, person, role) * weight)
            total_weight += weight

        return score / total_weight

    @abstractmethod
    def generate_roster(self, roster_sequence_no: int) -> Roster:
        """
        Generates a roster.

        :param roster_sequence_no: Sequence number of the assignment.
        :return: The generated roster.
        """
        pass

    def roster_score(self, roster: Roster) -> float:
        """
        Evaluates the quality of a roster.

        :param roster: Roster to evaluate.
        :return: A score. The higher the score, the better the assignment.
        """
        if len(roster.persons) == 0:
            return 0.0

        score = 0.0
        for person, role in roster.assignments.items():
            score += self.assignment_score(roster.sequence_no, person, role)

        return score / len(roster.persons)
