from dataset.Object import Object


class Absence(Object):

    def __init__(self, person_identifier: str, roster_sequence_no: int) -> None:
        """
        Constructor.

        :param person_identifier: Identifier of the absent person.
        :param roster_sequence_no: Sequence number of the roster in which the person will be absent.
        """
        super().__init__()

        self.set_value("person_identifier", person_identifier)
        self.set_value("roster_sequence_no", roster_sequence_no)

    @property
    def person_identifier(self) -> str:
        """
        Person identifier.
        """
        return self.get_value("person_identifier")

    @property
    def roster_sequence_no(self) -> int:
        """
        Roster sequence number.
        """
        return self.get_value("roster_sequence_no")
