from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Absence:
    """
    Represents an an absence of a person for a given roster.
    """

    person_identifier: str
    roster_sequence_no: int
