from dataset.Object import Object
from dataset.objects.Person import Person


class Roster(Object):

    def __init__(self, sequence_no: int, assignments: list[tuple[Person, str]] = None) -> None:
        """
        Constructor.

        :param sequence_no: Sequence number of the roster.
        :param assignments: Assignments of the roster.
        """
        super().__init__()
        self.set_value("sequence_no", sequence_no)
        self.set_value("assignments", assignments or {})

    def __str__(self):
        assignments = self.assignments.items()
        return "\n".join(map(lambda a: str(a[0]) + ": " + a[1], assignments))

    @property
    def assignments(self) -> dict[Person, str]:
        """
        Get the list of assignments.

        :return: A list of Person-Role tuples.
        """
        return self.get_value("assignments")

    @property
    def persons(self) -> list[Person]:
        """
        Gets the list of persons scheduled in this roster.

        :return: A list of person.
        """
        return list(self.assignments.keys())

    @property
    def sequence_no(self) -> int:
        """
        Returns the sequence number of the roster.

        :return: The sequence number.
        """
        return self.get_value("sequence_no")

    def assign(self, person: Person, role: str) -> None:
        """
        Assigns a person to a role.

        :param person: The person.
        :param role: The role.
        """
        assignments = self.assignments
        assignments[person] = role
        self.set_value("assignments", assignments)

    def get_role(self, person: Person) -> str:
        """
        Returns the role of a person.

        :param person: The person.
        :return: The role or None if the person is not scheduled.
        """
        person_identifier = person.identifier

        for current_person, role in self.assignments.items():
            if current_person is not None and person_identifier == current_person.identifier:
                return role

        return None

    def is_assigned(self, person: Person, role: str = None) -> bool:
        """
        Checks if a person is assigned in this roster.

        :param person: The person.
        :param role: The role. If not given, does not consider the role assigned to the person.
        :return: True if the person is assigned, false otherwise.
        """
        role_assigned = self.get_role(person)
        return role_assigned == role if role is not None else role_assigned is not None

    def remove_person(self, person: Person) -> None:
        """
        Removes a person from the roster.

        :param person: Person to remove.
        """
        assignments = self.assignments
        assignments.pop(person)
        self.set_value("assignments", assignments)
