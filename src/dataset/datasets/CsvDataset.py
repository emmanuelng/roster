import csv
from os import path

from dataset.dataclasses.Absence import Absence
from dataset.dataclasses.Pattern import Pattern
from dataset.dataclasses.Person import Person
from dataset.dataclasses.Roster import Roster
from dataset.datasets.ArrayDataset import ArrayDataset


class CsvDataset(ArrayDataset):
    """
    A dataset that stores the data in JSON files.
    """

    __directory: str

    def __init__(self, directory: str = "./data") -> None:
        """
        Constructor.

        :param directory: Path of the directory containing the CSV files.
        """
        super().__init__()

        self.__directory = directory

        self.__read_absences()
        self.__read_patterns()
        self.__read_persons()
        self.__read_rosters()

    def __del__(self):
        self.__save_absences()
        self.__save_patterns()
        self.__save_persons()
        self.__save_rosters()

    def __read_absences(self) -> None:
        """
        Loads the list of absences from absences.csv.
        """
        self._absences.clear()

        rows, nb_rows = self._read_csv_file("absences.csv")
        for row_index in range(nb_rows):
            roster_sequence_no, person_identifier = rows[row_index]
            self._absences.append(Absence(roster_sequence_no, person_identifier))

    def __read_patterns(self) -> None:
        """
        Loads the list of patterns from patterns.csv.
        """
        # Clear the current list.
        self._patterns.clear()

        # Read the dataset file.
        rows, nb_rows = self._read_csv_file("patterns.csv")

        for row_index in range(nb_rows):
            identifier, *assignments = rows[row_index]
            assignment_dict = {}

            for i in range(0, len(assignments), 2):
                assignment_dict[assignments[i]] = int(assignments[i + 1])

            pattern = Pattern(identifier, assignment_dict)
            self._patterns.append(pattern)

    def __read_persons(self) -> None:
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
                persons_by_id[identifier] = person

            # Set the list of persons.
            self._persons = list(persons_by_id.values())
        except ValueError:
            raise SyntaxError("Syntax error in persons.csv near line " + str(row_index + 1))

    def __read_rosters(self) -> None:
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
        file_path = f"{self.__directory}\\{file_name}"
        if not path.isfile(file_path):
            return [], 0

        with open(file_path) as file:
            rows = list(csv.reader(file))
            return rows, len(rows)

    def __save_absences(self) -> None:
        """
        Saves the list of absences.
        """
        rows = []

        for absence in self._absences:
            row = [absence.roster_sequence_no, absence.person_identifier]
            rows.append(row)

        self._write_csv_file("absences.csv", rows)

    def __save_patterns(self) -> None:
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

    def __save_rosters(self) -> None:
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

    def __save_persons(self) -> None:
        """
        Saves the list of persons.
        """
        rows = []

        for person in sorted(self._persons, key=lambda p: p.full_name):
            identifier = person.identifier
            f_name = person.first_name
            l_name = person.last_name

            rows.append([identifier, f_name, l_name] + person.roles)

        self._write_csv_file("persons.csv", rows)

    def _write_csv_file(self, file_name: str, rows: list[list[str]]) -> None:
        """
        Writes rows in a CSV file.

        :param file_name: Name of the file.
        :param rows: Rows to write.
        """
        with open(f"{self.__directory}\\{file_name}", "w") as file:
            file.write("\n".join(map(lambda r: ",".join(r), rows)))
