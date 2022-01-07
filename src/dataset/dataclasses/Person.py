from dataclasses import dataclass, field


@dataclass(frozen=True)
class Person:
    """
    Represents a person.
    """

    identifier: str = field(repr=False)
    first_name: str = field(hash=False)
    last_name: str = field(hash=False)
    roles: list[str] = field(hash=False, default_factory=list)

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
