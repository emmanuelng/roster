from typing import Optional

from database.Database import Database
from database.dataclasses.Absence import Absence
from database.dataclasses.Pattern import Pattern
from database.dataclasses.Person import Person
from database.dataclasses.Roster import Roster
from database.errors.DuplicateKeyError import DuplicateKeyError
from database.errors.ObjectNotFoundError import ObjectNotFoundError


class ListDataset(Database):
    """
    A simple database that uses python lists to store the data.
    """

    _persons: list[Person]
    _patterns: list[Pattern]
    _rosters: list[Roster]
    _absences: list[Absence]

    def __init__(self) -> None:
        """
        Constructor.
        """
        self._persons = []
        self._patterns = []
        self._rosters = []
        self._absences = []

    def add_absence(self, roster_sequence_no: int, person: Person):
        if len(self.get_absences(roster_sequence_no=roster_sequence_no, person=person)) == 0:
            self._absences.append(Absence(person.identifier, roster_sequence_no))

    def add_pattern(self, pattern: Pattern) -> None:
        if len(self.get_patterns(identifier=pattern.identifier)) > 0:
            raise DuplicateKeyError()

        self._patterns.append(pattern)

    def add_person(self, person: Person) -> None:
        if len(self.get_persons(identifier=person.identifier)) > 0:
            raise DuplicateKeyError()

        self._persons.append(person)

    def add_roster(self, roster: Roster) -> None:
        if len(self.get_rosters(sequence_no=roster.sequence_no)) > 0:
            raise DuplicateKeyError()

        self._rosters.append(roster)

    def get_absences(self, person: Person = None, roster_sequence_no: int = None) -> list[Absence]:
        absences = self._absences

        if person is not None:
            absences = filter(lambda a: a.person_identifier == person.identifier, absences)

        if roster_sequence_no is not None:
            absences = filter(lambda a: a.roster_sequence_no == roster_sequence_no, absences)

        return list(absences)

    def get_available_persons(self, roster_sequence_no: int, role: str = None) -> list[Person]:
        persons = self.get_persons(role=role)

        for absence in self.get_absences(roster_sequence_no=roster_sequence_no):
            persons = filter(lambda p: p.identifier != absence.person_identifier, persons)

        return list(persons)

    def get_pattern(self, identifier: str) -> Pattern:
        patterns = self.get_patterns(identifier=identifier)
        if len(patterns) == 0:
            raise ObjectNotFoundError()

        return patterns[0]

    def get_patterns(self, identifier: str = None) -> list[Pattern]:
        patterns = self._patterns

        if identifier is not None:
            patterns = filter(lambda p: p.identifier == identifier, patterns)

        return list(patterns)

    def get_person(self, identifier: str) -> Person:
        persons = self.get_persons(identifier=identifier)
        if len(persons) == 0:
            raise ObjectNotFoundError()

        return persons[0]

    def get_persons(self, identifier: str = None, role: str = None) -> list[Person]:
        persons = self._persons

        if identifier is not None:
            persons = filter(lambda p: p.identifier == identifier, persons)

        if role is not None:
            persons = filter(lambda p: p.has_role(role), persons)

        return list(persons)

    def get_roster(self, sequence_no: int) -> Optional[Roster]:
        rosters = self.get_rosters(sequence_no=sequence_no)
        if len(rosters) <= 0:
            raise ObjectNotFoundError()

        return rosters[0]

    def get_rosters(self, sequence_no: int = None, before: int = None, after: int = None) -> list[Roster]:
        rosters = self._rosters

        if sequence_no is not None:
            rosters = filter(lambda r: r.sequence_no == sequence_no, rosters)

        if before is not None:
            rosters = filter(lambda r: r.sequence_no < before, rosters)

        if after is not None:
            rosters = filter(lambda r: r.sequence_no > after, rosters)

        return list(rosters)

    def remove_absence(self, roster_sequence_no: int, person: Person) -> None:
        self._absences = filter(
            lambda a: a.roster_sequence_no != roster_sequence_no and a.person_identifier != person.identifier,
            self._absences
        )

    def remove_pattern(self, identifier: str) -> None:
        self._patterns = list(filter(lambda p: p.identifier != identifier, self._patterns))

    def remove_person(self, identifier: str) -> None:
        self._persons = list(filter(lambda p: p.identifier != identifier, self._persons))

    def remove_roster(self, sequence_no: int) -> None:
        self._rosters = list(filter(lambda r: r.sequence_no != sequence_no, self._rosters))
