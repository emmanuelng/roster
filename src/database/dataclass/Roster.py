from typing import Optional

from database.Dataclass import Dataclass, Field
from database.dataclass.Person import Person


class Roster(Dataclass):
    """
    Represents a roster. A roster indicates which persons are assigned for which roles at a given date.
    """

    sequence_no: int
    assignments: dict[str, str] = Field(key=False, default_factory=dict)

    @property
    def persons(self) -> list[Person]:
        """
        List of persons assigned in this roster.
        """
        return list(self.assignments.keys())

    def get_role(self, person: Person) -> Optional[str]:
        """
        Returns the role of a person.

        :param person: The person.
        :return: The role or None if the person is not scheduled.
        """
        person_assignments = [a for a in self.assignments.items() if a[0] == person.identifier]
        return person_assignments[0][1] if person_assignments else None

    def is_assigned(self, person: Person, role: str = None) -> bool:
        """
        Checks if a person is assigned in this roster.

        :param person: The person.
        :param role: The role. If not given, does not consider the role assigned to the person.
        :return: True if the person is assigned, false otherwise.
        """
        role_assigned = self.get_role(person)
        return role_assigned == role if role is not None else role_assigned is not None
