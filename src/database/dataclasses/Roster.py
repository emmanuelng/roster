from dataclasses import dataclass, field
from typing import Optional

from database.dataclasses.Person import Person


@dataclass(order=True)
class Roster:
    """
    Represents a roster. A roster indicates which persons are assigned for which roles at a given date.
    """

    sequence_no: int
    assignments: dict[Person, str] = field(default_factory=dict, compare=False)

    @property
    def persons(self) -> list[Person]:
        return list(self.assignments.keys())

    def assign(self, person: Person, role: str) -> None:
        """
        Assigns a person to a role.

        :param person: The person.
        :param role: The role.
        """
        self.assignments[person] = role

    def get_role(self, person: Person) -> Optional[str]:
        """
        Returns the role of a person.

        :param person: The person.
        :return: The role or None if the person is not scheduled.
        """
        assignment_tuple = next(a for a in self.assignments.items() if a[0].identifier == person.identifier)
        return assignment_tuple[1] if assignment_tuple is not None else None

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
        self.assignments.pop(person)
