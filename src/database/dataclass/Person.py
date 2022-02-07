from database.Dataclass import Dataclass, Field


class Person(Dataclass):
    """
    Represents a person.
    """

    identifier: str
    last_name: str = Field(key=False)
    first_name: str = Field(key=False)
    roles: list[str] = Field(key=False, default_factory=list)

    @property
    def full_name(self) -> str:
        """
        Returns the full name of the person.

        :return: A string with the full name of the person.
        """
        return f"{self.first_name} {self.last_name}"

    def has_role(self, role: str) -> bool:
        """
        Checks if this person has a role.

        :param role: The role
        :return: True if the person has the role, false otherwise.
        """
        return role in self.roles
