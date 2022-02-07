from app.Context import Context
from app.Resource import Resource, Action
from database.dataclass.Absence import Absence


class RosterAbsences(Resource):

    def __init__(self) -> None:
        super().__init__()

        # Methods
        self._method("get", Action.GET, self.get)

    @staticmethod
    def get(context: Context, roster_sequence_no: str) -> list[Absence]:
        """
        Get the absences of a roster.
        """
        return context.database.get(Absence, roster_sequence_no=int(roster_sequence_no))
