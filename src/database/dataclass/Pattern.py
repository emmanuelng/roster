from database.Dataclass import Dataclass, Field


class Pattern(Dataclass):
    """
    Roster pattern. Represents a pattern that can be used to generate a roster. A pattern defines the roles that are
    needed and the number of persons required for each of them.
    """

    identifier: str
    assignments: dict[str, int] = Field(key=False, default_factory=dict)

    @property
    def roles(self) -> list[str]:
        """
        Pattern roles.
        """
        return list(self.assignments.keys())
