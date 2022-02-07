from app.Context import Context
from app.Resource import Resource, Action
from database.dataclass.Person import Person
from database.dataclass.Roster import Roster


class RosterAssignments(Resource):

    def __init__(self) -> None:
        super().__init__()

        # Methods
        self._method("create", Action.CREATE, self.create)
        self._method("delete", Action.DELETE, self.delete)

    @staticmethod
    def create(context: Context, roster_sequence_no: str, person_id: str, role: str) -> None:
        """
        Assign a person to a role.
        """
        roster = context.database.get_unique(Roster, sequence_no=int(roster_sequence_no))
        person = context.database.get(Person, identifier=person_id)

        assignments = roster.assignments
        assignments[role] = person_id
        roster.assign(person, role)

    @staticmethod
    def delete(context: Context, roster_sequence_no: str, person_id: str) -> None:
        """
        Remove a person from a roster.
        """
        roster = context.database.get_unique(Roster, sequence_no=int(roster_sequence_no))
        roster.remove_person(person_id)
