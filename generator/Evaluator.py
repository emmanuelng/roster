from abc import ABC, abstractmethod

from dataset.objects.Person import Person


class Evaluator(ABC):

    @abstractmethod
    def assignment_score(self, roster_sequence_no: int, person: Person, role: str) -> float:
        """
        Evaluates an assignment in a roster.

        :param roster_sequence_no: The sequence number of the roster.
        :param person: The person.
        :param role: The role of the person.
        :return: A score between 0 and 1. A score of 0 indicates that the assignment is not recommended, 1 indicates
         that it is strongly recommended.
        """
        pass
