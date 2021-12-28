from dataclasses import dataclass


@dataclass(frozen=True)
class Pattern:
    """
    Roster pattern. Represents a pattern that can be used to generate a roster. A pattern defines the roles that are
    needed and the number of persons required for each of them.
    """

    identifier: str
    assignments: dict[str, int]