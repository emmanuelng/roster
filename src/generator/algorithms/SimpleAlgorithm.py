from typing import Optional

from database.dataclass.Absence import Absence
from database.dataclass.Pattern import Pattern
from database.dataclass.Person import Person
from database.dataclass.Roster import Roster
from generator import Generator
from generator.Algorithm import Algorithm
from generator.errors.NotEnoughResourcesError import NotEnoughResourcesError


class SimpleAlgorithm(Algorithm):
    """
    Simple algorithm. The simplest algorithm. For each pattern, goes through the list of roles and picks the best
    persons for each of them. The solution depends on the order of the roles in the pattern and might not be optimal.
    """

    def __init__(self, generator: Generator) -> None:
        """
        Constructor.

        :param generator: Generator associated to this algorithm.
        """
        super().__init__(generator)

    def generate_roster(self, roster_sequence_no: int) -> Roster:
        best_score, best_roster = None, None

        for pattern in self.database.get(Pattern):
            try:
                roster = self.__generate_roster_with_pattern(roster_sequence_no, pattern)
                score = self.roster_score(roster)

                if best_score is None or score > best_score:
                    best_score, best_roster = score, roster
            except NotEnoughResourcesError:
                continue

        if best_roster is None:
            raise NotEnoughResourcesError()

        return best_roster

    def __generate_roster_with_pattern(self, sequence_no: int, pattern: Pattern) -> Optional[Roster]:
        """
        Generates a roster with the given pattern.

        :param sequence_no: Sequence number of the roster.
        :param pattern: Pattern to use.
        :return: A roster.
        """
        roster = Roster(sequence_no=sequence_no)

        for role in pattern.roles:
            number = pattern.assignments[role]
            self.__assign_persons_for_role(roster, role, number)

        return roster

    def __assign_persons_for_role(self, roster: Roster, role: str, number: int) -> None:
        """
        Finds and assigns persons for a given role.

        :param roster: The roster.
        :param role: The role.
        :param number: Number of persons required for the role.
        """
        if number == 0:
            return

        persons = self.__find_persons_for_role(roster, role)
        person_to_assign = max(persons, key=lambda p: self.assignment_score(roster.sequence_no, p, role))
        roster.assign(person_to_assign, role)

        self.__assign_persons_for_role(roster, role, number - 1)

    def __find_persons_for_role(self, roster: Roster, role: str) -> list[Person]:
        """
        Returns the list of persons that can do a role in a roster.

        :param roster: The roster.
        :param role: The role
        :return: A list of persons.
        """
        persons = self.__get_available_persons(roster.sequence_no)
        persons = filter(lambda p: p.has_role(role), persons)
        persons = list(filter(lambda p: not roster.is_assigned(p), persons))

        if len(persons) == 0:
            raise NotEnoughResourcesError()

        return persons

    def __get_available_persons(self, roster_sequence_no) -> list[Person]:
        """
        Gets the list of all persons that are available for a roster.

        :param roster_sequence_no: Sequence number of the roster.
        :return: A list of persons.
        """
        available_persons = []
        absences = self.database.get(Absence, roster_sequence_no=roster_sequence_no)

        for person in self.database.get(Person):
            is_available = True
            for absence in absences:
                if absence.person_identifier == person.identifier:
                    is_available = False
                    break
            if is_available:
                available_persons.append(person)

        return available_persons
