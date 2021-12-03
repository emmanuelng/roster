from typing import Optional

from dataset.objects.Pattern import Pattern
from dataset.objects.Person import Person
from dataset.objects.Roster import Roster
from generator import Generator
from generator.Algorithm import Algorithm
from generator.errors.NotEnoughResourcesError import NotEnoughResourcesError


class SimpleAlgorithm(Algorithm):

    def __init__(self, generator: Generator) -> None:
        """
        Constructor.

        :param generator: Generator associated to this algorithm.
        """
        super().__init__(generator)

    def generate_roster(self, roster_sequence_no: int) -> Roster:
        best_score, best_roster = None, None

        for pattern in self.dataset.get_patterns():
            try:
                roster = self._generate_roster_with_pattern(roster_sequence_no, pattern)
                score = self.roster_score(roster)

                if best_score is None or score > best_score:
                    best_score, best_roster = score, roster
            except NotEnoughResourcesError:
                continue

        if best_roster is None:
            raise NotEnoughResourcesError()

        return best_roster

    def _generate_roster_with_pattern(self, sequence_no: int, pattern: Pattern) -> Optional[Roster]:
        """
        Generates a roster with the given pattern.

        :param sequence_no: Sequence number of the roster.
        :param pattern: Pattern to use.
        :return: A roster.
        """
        roster = Roster(sequence_no)

        for role in pattern.roles:
            number = pattern.get_number(role)
            self._assign_persons_for_role(roster, role, number)

        return roster

    def _assign_persons_for_role(self, roster: Roster, role: str, number: int) -> None:
        """
        Finds and assigns persons for a given role.

        :param roster: The roster.
        :param role: The role.
        :param number: Number of persons required for the role.
        """
        if number == 0:
            return

        persons = self._find_persons_for_role(roster, role)
        person_to_assign = max(persons, key=lambda p: self.assignment_score(roster.sequence_no, p, role))
        roster.assign(person_to_assign, role)

        self._assign_persons_for_role(roster, role, number - 1)

    def _find_persons_for_role(self, roster: Roster, role: str) -> list[Person]:
        """
        Returns the list of persons that can do a role in a roster.

        :param roster: The roster.
        :param role: The role
        :return: A list of persons.
        """
        persons = self.dataset.get_available_persons(roster.sequence_no, role=role)
        persons = list(filter(lambda p: not roster.is_assigned(p), persons))

        if len(persons) == 0:
            raise NotEnoughResourcesError()

        return persons
