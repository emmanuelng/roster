from database.Dataclass import Dataclass


class Absence(Dataclass):
    """
    Represents an an absence of a person for a given roster.
    """

    person_identifier: str
    roster_sequence_no: int
