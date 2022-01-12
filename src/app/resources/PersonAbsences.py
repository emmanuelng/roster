from typing import Union

from app.Context import Context
from app.Resource import Resource, Action
from app.errors.InvalidArgumentError import InvalidArgumentError
from database.dataclasses.Absence import Absence


class PersonAbsences(Resource):

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
    def create(context: Context, person_id: str, roster_sequence_no: Union[str, int]) -> Absence:
        """
        Create a new absence.

        :param context: The context.
        :param person_id: Identifier of the person.
        :param roster_sequence_no: Sequence number of the roster.
        :return: The newly created absence.
        """
        try:
            absence = Absence(roster_sequence_no=int(roster_sequence_no), person_identifier=person_id)
            context.database.add_absence(absence)
            return absence
        except ValueError:
            raise InvalidArgumentError("roster_sequence_no")

    @staticmethod
    def delete(context: Context, person_id: str, roster_sequence_no: Union[str, int]) -> None:
        """
        Delete an absence.

        :param context: The context.
        :param person_id: Identifier of the person.
        :param roster_sequence_no: Sequence number of the roster.
        """
        person = context.database.get_person(person_id)
        context.database.remove_absence(int(roster_sequence_no), person)

    @staticmethod
    def list(context: Context, person_id: str) -> list[Absence]:
        """
        Get the absences of a person.

        :param context: The context.
        :param person_id: Identifier of the person.
        :return: A list of absences, sorted by roster sequence number.
        """
        person = context.database.get_person(person_id)
        absences = context.database.get_absences(person=person)
        absences.sort()
        return absences
