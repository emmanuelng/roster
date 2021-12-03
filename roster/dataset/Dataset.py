import csv
import os.path
from builtins import ValueError, open
from typing import Optional

from dataset.errors.ObjectNotFoundError import ObjectNotFoundError
from dataset.objects.Pattern import Pattern
from dataset.objects.Person import Person
from dataset.objects.Roster import Roster


class Dataset:

    def __init__(self, directory: str = "./data") -> None:
        """
        Constructor.

        :param directory: Path of the directory containing the dataset files.
        """
        self._directory = directory
        self._persons = []
        self._patterns = []
        self._rosters = []
        self._absences = {}

        # Load dataset files.
        self._read_absences()
        self._read_patterns()
        self._read_persons()
        self._read_rosters()

    def add_absence(self, roster_sequence_no: int, person: Person):
        """
        Adds an absence.

        :param roster_sequence_no: Sequence number of the roster in which the person will be absent.
        :param person: The absent person.
        """
        if roster_sequence_no not in self._absences:
            self._absences[roster_sequence_no] = []

        if person.identifier not in self._absences[roster_sequence_no]:
            self._absences[roster_sequence_no].append(person.identifier)
            self._save_absences()

    def add_pattern(self, pattern: Pattern) -> None:
        """
        Adds a pattern to the list of patterns.

        :param pattern: Pattern to add.
        """
        if self.get_pattern(pattern.identifier) is not None:
            raise Exception("A pattern with the same identifier already exists.")

        pattern.on_modify(lambda: self._save_patterns())
        self._patterns.append(pattern)
        self._save_patterns()

    def add_person(self, person: Person) -> None:
        """
        Adds a person to the list of persons.

        :param person: Person to add.
        """
        if self.get_person(person.identifier) is not None:
            raise Exception("A person with the same identifier already exists.")

        person.on_modify(lambda: self._save_persons())
        self._persons.append(person)
        self._save_persons()

    def add_roster(self, roster: Roster) -> None:
        """
        Adds a roster to the list of rosters.

        :param roster: The roster to add.
        """
        if (self.get_roster(roster.sequence_no)) is not None:
            raise Exception("A roster with the same sequence number already exists.")

        roster.on_modify(lambda: self._save_rosters())
        self._rosters.append(roster)
        self._save_rosters()

    def get_available_persons(self, roster_sequence_no: int, role: str = None) -> list[Person]:
        """
        Returns the list of available persons for a roster.

        :param roster_sequence_no: Sequence number of the roster.
        :param role: If given, only returns the persons with this role.
        :return: A list of persons.
        """
        persons = self.get_persons(role=role)
        absences = self._absences.get(roster_sequence_no, [])
        return list(filter(lambda p: p.identifier not in absences, persons))

    def get_pattern(self, identifier: str) -> Pattern:
        """
        Finds a pattern using an identifier.

        :return: The pattern or None if the identifier doesn't exist.
        """
        return next((p for p in self._patterns if p.identifier == identifier), None)

    def get_patterns(self) -> list[Pattern]:
        """
        Returns the list of patterns.

        :return: A list of patterns.
        """
        return self._patterns

    def get_person(self, identifier: str) -> Person:
        """
        Finds the person with the given identifier.

        :return: The Person or None if the identifier doesn't exist.
        """
        person = next((p for p in self._persons if p.identifier == identifier), None)
        if person is None:
            raise ObjectNotFoundError()

        return person

    def get_person_absences(self, person: Person) -> list[int]:
        """
        Returns the list of rosters in which a person will be absent.

        :param person: The person.
        :return: List of roster sequence numbers.
        """
        rosters = []
        for roster_sequence_no, persons in self._absences.items():
            if person.identifier in persons:
                rosters.append(roster_sequence_no)

        return rosters

    def get_roster_absences(self, roster_sequence_no: int) -> list[Person]:
        """
        Get the persons that will be absent for a given roster.

        :param roster_sequence_no: Sequence number of the roster.
        :return: The list of absent persons.
        """
        return self._absences.get(roster_sequence_no, [])

    def get_persons(self, identifier: str = None, role: str = None) -> list[Person]:
        """
        Returns the list of persons.

        :param identifier: If given, only returns the person with this identifier.
        :param role: If given, only returns the persons with this role.
        :return: A list of persons.
        """
        persons = self._persons

        # Filter by identifier.
        if identifier is not None:
            persons = filter(lambda p: p.identifier == identifier, persons)

        # Filter by role.
        if role is not None:
            persons = filter(lambda p: p.has_role(role), persons)

        return list(persons)

    def get_roster(self, sequence_no: int) -> Optional[Roster]:
        """
        Finds the roster with the given sequence number.

        :param sequence_no: The sequence number.
        :return: The roster or None if it does not exist.
        """
        rosters = self.get_rosters(sequence_no=sequence_no)
        if len(rosters) <= 0:
            raise ObjectNotFoundError()

        return rosters[0]

    def get_rosters(self, sequence_no: int = None, before: int = None, after: int = None) -> list[Roster]:
        """
        Returns the list of rosters.

        :param sequence_no: If given, only returns the roster with this sequence number.
        :param before: If given, only returns the rosters before this sequence number.
        :param after: If given, only returns the rosters after this sequence number.
        :return: A list of rosters.
        """
        rosters = self._rosters

        # Filter by sequence number.
        if sequence_no is not None:
            rosters = filter(lambda r: r.sequence_no == sequence_no, rosters)

        # Filter the rosters before the given sequence number.
        if before is not None:
            rosters = filter(lambda r: r.sequence_no < before, rosters)

        # Filter the rosters after the given sequence number.
        if after is not None:
            rosters = filter(lambda r: r.sequence_no > after, rosters)

        return list(rosters)

    def remove_absence(self, roster_sequence_no: int, person: Person) -> None:
        """
        Removes an absence.

        :param roster_sequence_no: Sequence number of the roster in which the person will be absent.
        :param person: The absent person.
        """
        if roster_sequence_no not in self._absences:
            return

        if person.identifier not in self._absences[roster_sequence_no]:
            return

        self._absences[roster_sequence_no].remove(person.identifier)
        self._save_absences()

    def remove_pattern(self, identifier: str) -> None:
        """
        Removes a pattern from the list of patterns.

        :param identifier: Identifier of the patterns.
        """
        self._patterns = filter(lambda p: p.identifier != identifier, self._patterns)
        self._save_patterns()

    def remove_person(self, identifier: str) -> None:
        """
        Removes a person from the list of persons.
        :param identifier: Identifier of the person.
        """
        self._persons = filter(lambda p: p.identifier != identifier, self._persons)
        self._save_persons()

    def remove_roster(self, sequence_no: int) -> None:
        """
        Removes a roster from the list of rosters.

        :param sequence_no: Identifier of the roster.
        """
        self._rosters = filter(lambda r: r.sequence_no != sequence_no, self._rosters)
        self._save_rosters()

    def _read_absences(self) -> None:
        """
        Loads the list of absences from absences.csv.
        """
        self._absences.clear()

        rows, nb_rows = self._read_csv_file("absences.csv")
        for row_index in range(nb_rows):
            roster_sequence_no, *persons_id_list = rows[row_index]
            self._absences[int(roster_sequence_no)] = persons_id_list

    def _read_patterns(self) -> None:
        """
        Loads the list of patterns from patterns.csv.
        """
        # Clear the current list.
        self._patterns.clear()

        # Read the dataset file.
        rows, nb_rows = self._read_csv_file("patterns.csv")

        for row_index in range(nb_rows):
            identifier, *assignments = rows[row_index]

            pattern = Pattern(identifier)

            for i in range(0, len(assignments), 2):
                pattern.set_assignment(assignments[i], int(assignments[i + 1]))

            pattern.on_modify(lambda: self._save_patterns())
            self._patterns.append(pattern)

    def _read_persons(self) -> None:
        """
        Loads the list of persons from persons.csv.
        """
        # Clear the current list
        self._persons.clear()

        # Read the dataset file.
        rows, nb_rows = self._read_csv_file("persons.csv")

        # Read the lines of each person and build the person objects.
        row_index = 0
        try:
            persons_by_id = {}

            for row_index in range(nb_rows):
                identifier, first_name, last_name, *roles = rows[row_index]

                person = Person(identifier, first_name, last_name, roles)
                person.on_modify(lambda: self._save_persons())

                persons_by_id[identifier] = person

            # Set the list of persons.
            self._persons = list(persons_by_id.values())
        except ValueError:
            raise SyntaxError("Syntax error in persons.csv near line " + str(row_index + 1))

    def _read_rosters(self) -> None:
        """
        Loads the list of rosters from rosters.csv.
        """
        # Clear the current list
        self._rosters.clear()

        # Read the dataset file.
        rows, nb_rows = self._read_csv_file("rosters.csv")
        roster_by_sequence_no = {}

        row_index = 0
        try:
            for row_index in range(nb_rows):
                sequence_no, *assignments = rows[row_index]
                roster = Roster(int(sequence_no))

                for j in range(0, len(assignments) - 1, 2):
                    person, role = self.get_person(assignments[j]), assignments[j + 1]
                    roster.assign(person, role)

                roster.on_modify(lambda: self._save_rosters())
                roster_by_sequence_no[sequence_no] = roster

            self._rosters = list(roster_by_sequence_no.values())
        except ValueError:
            raise SyntaxError("Syntax error in rosters.csv near line " + str(row_index + 1))

    def _read_csv_file(self, file_name: str) -> (list[str], int):
        """
        Reads and parses a CSV file in the data directory.

        :param file_name: Name of the file with its extension.
        :return: A list of strings corresponding to the lines of the file.
        """
        # Check that the file exists.
        file_path = self._directory + "\\" + file_name
        if not os.path.isfile(file_path):
            return [], 0

        # Parse the file.
        rows = list(csv.reader(open(file_path)))
        return rows, len(rows)

    def _save_absences(self) -> None:
        """
        Saves the list of absences.
        """
        rows = []

        for roster_sequence_no, persons in self._absences.items():
            if len(persons) > 0:
                row = [str(roster_sequence_no)] + persons
                rows.append(row)

        self._write_csv_file("absences.csv", rows)

    def _save_patterns(self) -> None:
        """
        Saves the list of patterns.
        """
        rows = []

        for pattern in self._patterns:
            row = [pattern.identifier]
            for assignment in pattern.assignments.items():
                row += [assignment[0], str(assignment[1])]

            rows.append(row)

        self._write_csv_file("patterns.csv", rows)

    def _save_rosters(self) -> None:
        """
        Saves the rosters.
        """
        rows = []

        for roster in sorted(self._rosters, key=lambda r: r.sequence_no):
            row = [str(roster.sequence_no)]
            for person in roster.persons:
                row += [person.identifier, roster.get_role(person)]
            rows += [row]

        self._write_csv_file("rosters.csv", rows)

    def _save_persons(self) -> None:
        """
        Saves the list of persons.
        """
        rows = []

        for person in sorted(self._persons, key=lambda p: p.full_name):
            identifier = person.identifier
            f_name = person.first_name
            l_name = person.last_name

            rows.append([identifier, f_name, l_name] + person.person_roles_get())

        self._write_csv_file("persons.csv", rows)

    def _write_csv_file(self, file_name: str, rows: list[list[str]]) -> None:
        """
        Writes rows in a CSV file.

        :param file_name: Name of the file.
        :param rows: Rows to write.
        """
        file_path = self._directory + "\\" + file_name
        file = open(file_path, "w")
        file.write("\n".join(map(lambda r: ",".join(r), rows)))
        file.close()
