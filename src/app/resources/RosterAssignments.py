from typing import Union

from app.Context import Context
from app.Resource import Resource, Action
from app.errors.InvalidArgumentError import InvalidArgumentError
from database.dataclass.Person import Person
from database.dataclass.Roster import Roster


class RosterAssignments(Resource):

    def __init__(self) -> None:
        """
        Constructor.
        """
        super().__init__()

        # Methods
        self._method("create", Action.CREATE, self.create)
        self._method("delete", Action.DELETE, self.delete)

    @staticmethod
    def create(context: Context, roster_sequence_no: Union[int, str], person_id: str, role: str) -> None:
        """
        Assign a person to a role.

        :param context: The context.
        :param roster_sequence_no: Roster sequence number.
        :param person_id: Person identifier.
        :param role: Role of the person.
        """
        if not role:
            raise InvalidArgumentError("role")

        try:
            roster: Roster = context.database.get_unique(Roster, sequence_no=int(roster_sequence_no))
            person: Person = context.database.get_unique(Person, identifier=person_id)

            assignments = roster.assignments
            assignments[person.identifier] = role
            context.database.update(roster, assignments=assignments)
        except ValueError:
            raise InvalidArgumentError("roster_sequence_no")

    @staticmethod
    def delete(context: Context, roster_sequence_no: Union[int, str], person_id: str) -> None:
        """
        Delete an assignment.

        :param context: The context.
        :param roster_sequence_no: Roster sequence number.
        :param person_id: Identifier of the person.
        """

        try:
            roster: Roster = context.database.get_unique(Roster, sequence_no=int(roster_sequence_no))
            person: Person = context.database.get_unique(Person, identifier=person_id)

            if person.identifier not in roster.assignments:
                return

            assignments = roster.assignments
            assignments.pop(person.identifier)
            context.database.update(roster, assignments=assignments)
        except ValueError:
            raise InvalidArgumentError("roster_sequence_no")
