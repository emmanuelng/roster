from abc import ABC, abstractmethod
from typing import Optional

from database.dataclasses.Absence import Absence
from database.dataclasses.Pattern import Pattern
from database.dataclasses.Person import Person
from database.dataclasses.Roster import Roster


class Database(ABC):
    """
    Represents a set of data used by the program. This class is responsible for reading and saving the data.
    """

    @abstractmethod
    def add_absence(self, roster_sequence_no: int, person: Person):
        """
        Adds an absence.

        :param roster_sequence_no: Sequence number of the roster in which the person will be absent.
        :param person: The absent person.
        """
        pass

    @abstractmethod
    def add_pattern(self, pattern: Pattern) -> None:
        """
        Adds a pattern to the list of patterns.

        :param pattern: Pattern to add.
        """
        pass

    @abstractmethod
    def add_person(self, person: Person) -> None:
        """
        Adds a person to the list of persons.

        :param person: Person to add.
        """
        pass

    @abstractmethod
    def add_roster(self, roster: Roster) -> None:
        """
        Adds a roster to the list of rosters.

        :param roster: The roster to add.
        """
        pass

    @abstractmethod
    def get_absences(self, person: Person = None, roster_sequence_no: int = None) -> list[Absence]:
        """
        Returns the absences corresponding to certain criteria.

        :param person: If provided, only returns the absences of this person.
        :param roster_sequence_no: If provided, only returns absences for this roster.
        :return: List of absences.
        """
        pass

    @abstractmethod
    def get_available_persons(self, roster_sequence_no: int, role: str = None) -> list[Person]:
        """
        Returns the list of available persons for a roster.

        :param roster_sequence_no: Sequence number of the roster.
        :param role: If given, only returns the persons with this role.
        :return: A list of persons.
        """
        pass

    @abstractmethod
    def get_pattern(self, identifier: str) -> Pattern:
        """
        Finds a pattern using an identifier.

        :return: The pattern or None if the identifier doesn't exist.
        """
        pass

    @abstractmethod
    def get_patterns(self) -> list[Pattern]:
        """
        Returns the list of patterns.

        :return: A list of patterns.
        """
        pass

    @abstractmethod
    def get_person(self, identifier: str) -> Person:
        """
        Finds the person with the given identifier.

        :return: The Person or None if the identifier doesn't exist.
        """
        pass

    @abstractmethod
    def get_persons(self, identifier: str = None, role: str = None) -> list[Person]:
        """
        Returns the list of persons.

        :param identifier: If given, only returns the person with this identifier.
        :param role: If given, only returns the persons with this role.
        :return: A list of persons.
        """
        pass

    @abstractmethod
    def get_roster(self, sequence_no: int) -> Optional[Roster]:
        """
        Finds the roster with the given sequence number.

        :param sequence_no: The sequence number.
        :return: The roster or None if it does not exist.
        """
        pass

    @abstractmethod
    def get_rosters(self, sequence_no: int = None, before: int = None, after: int = None) -> list[Roster]:
        """
        Returns the list of rosters.

        :param sequence_no: If given, only returns the roster with this sequence number.
        :param before: If given, only returns the rosters before this sequence number.
        :param after: If given, only returns the rosters after this sequence number.
        :return: A list of rosters.
        """
        pass

    @abstractmethod
    def remove_absence(self, roster_sequence_no: int, person: Person) -> None:
        """
        Removes an absence.

        :param roster_sequence_no: Sequence number of the roster in which the person will be absent.
        :param person: The absent person.
        """
        pass

    @abstractmethod
    def remove_pattern(self, identifier: str) -> None:
        """
        Removes a pattern from the list of patterns.

        :param identifier: Identifier of the patterns.
        """
        pass

    @abstractmethod
    def remove_person(self, identifier: str) -> None:
        """
        Removes a person from the list of persons.
        :param identifier: Identifier of the person.
        """
        pass

    @abstractmethod
    def remove_roster(self, sequence_no: int) -> None:
        """
        Removes a roster from the list of rosters.

        :param sequence_no: Identifier of the roster.
        """
        pass
