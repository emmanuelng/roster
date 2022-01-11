from dataclasses import dataclass, field


@dataclass
class Pattern:
    """
    Roster pattern. Represents a pattern that can be used to generate a roster. A pattern defines the roles that are
    needed and the number of persons required for each of them.
    """

    identifier: str
    assignments: dict[str, int] = field(default_factory=dict)

    @property
    def roles(self) -> list[str]:
        return self.assignments.keys()
