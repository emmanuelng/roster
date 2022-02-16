from typing import Union

from app.Context import Context
from app.Resource import Resource, Action
from app.errors.InvalidArgumentError import InvalidArgumentError
from database.dataclass.Absence import Absence
from database.dataclass.Person import Person


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
            person: Person = context.database.get_unique(Person, identifier=person_id)
            return context.database.create(Absence,
                                           roster_sequence_no=int(roster_sequence_no),
                                           person_identifier=person.identifier)
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
        person: Person = context.database.get_unique(Person, identifier=person_id)
        context.database.delete(Absence,
                                roster_sequence_no=int(roster_sequence_no),
                                person_identifier=person.identifier)

    @staticmethod
    def list(context: Context, person_id: str) -> list[Absence]:
        """
        Get the absences of a person.

        :param context: The context.
        :param person_id: Identifier of the person.
        :return: A list of absences, sorted by roster sequence number.
        """
        person: Person = context.database.get_unique(Person, identifier=person_id)
        absences: list[Absence] = context.database.get(Absence, person_identifier=person.identifier)
        absences.sort(key=lambda a: a.roster_sequence_no)
        return absences
