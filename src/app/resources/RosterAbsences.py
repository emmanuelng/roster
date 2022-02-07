from typing import Union

from app.Context import Context
from app.Resource import Resource, Action
from app.errors.InvalidArgumentError import InvalidArgumentError
from database.dataclass.Absence import Absence
from database.dataclass.Person import Person


class RosterAbsences(Resource):

    def __init__(self) -> None:
        """
        Constructor.
        """
        super().__init__()

        # Methods
        self._method("create", Action.CREATE, self.create)
        self._method("delete", Action.DELETE, self.delete)
        self._method("list", Action.GET, self.list)

    @staticmethod
    def create(context: Context, roster_sequence_no: Union[str, int], person_id: str) -> Absence:
        """
        Create a new absence.

        :param context: The context.
        :param roster_sequence_no: Sequence number of the roster.
        :param person_id: Identifier of the person.
        :return: The newly created absence.
        """
        try:
            person = context.database.get_unique(Person, identifier=person_id)
            return context.database.create(Absence,
                                           roster_sequence_no=int(roster_sequence_no),
                                           person_identifier=person.identifier)
        except ValueError:
            raise InvalidArgumentError("roster_sequence_no")

    @staticmethod
    def delete(context: Context, roster_sequence_no: Union[str, int], person_id: str) -> None:
        """
        Delete an absence.

        :param context: The context.
        :param roster_sequence_no: Sequence number of the roster.
        :param person_id: Identifier of the person.
        """
        try:
            context.database.get_unique(Person, identifier=person_id)
            context.database.delete(Absence, roster_sequence_no=int(roster_sequence_no), person_identifier=person_id)
        except ValueError:
            raise InvalidArgumentError("roster_sequence_no")

    @staticmethod
    def list(context: Context, roster_sequence_no: Union[str, int]) -> list[Absence]:
        """
        Get the absences of a roster.

        :param context: The context.
        :param roster_sequence_no: Roster sequence number.
        :return: A list of absences, sorted by person names.
        """
        try:
            absences = context.database.get(Absence, roster_sequence_no=int(roster_sequence_no))
            absences.sort(key=lambda a: context.database.get_unique(Person, identifier=a.person_identifier).full_name)
            return absences
        except ValueError:
            raise InvalidArgumentError("roster_sequence_no")
