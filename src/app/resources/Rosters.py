from typing import Union

from app.Context import Context
from app.Resource import Resource, Action
from app.errors.InvalidArgumentError import InvalidArgumentError
from app.resources.RosterAbsences import RosterAbsences
from app.resources.RosterAssignments import RosterAssignments
from configuration.Configuration import Configuration
from database.dataclasses.Roster import Roster
from generator.Generator import Generator


class Rosters(Resource):

    def __init__(self) -> None:
        """
        Constructor.
        """
        super().__init__()

        # Child resources
        self._child_resource("absences", RosterAbsences())
        self._child_resource("assignments", RosterAssignments())

        # Methods
        self._method("create", Action.CREATE, self.create)
        self._method("delete", Action.DELETE, self.delete)
        self._method("test", Action.CREATE, self.generate)
        self._method("get", Action.GET, self.get)
        self._method("list", Action.GET, self.list)

    @staticmethod
    def create(context: Context, sequence_no: Union[int, str]) -> Roster:
        """
        Create a new roster.

        :param context: The context.
        :param sequence_no: Sequence number of the roster.
        :return: The newly created roster.
        """
        try:
            roster = Roster(int(sequence_no))
            context.database.add_roster(roster)
            return roster
        except ValueError:
            raise InvalidArgumentError("sequence_no")

    @staticmethod
    def delete(context: Context, sequence_no: Union[int, str]) -> None:
        """
        Remove a roster.

        :param context: The context.
        :param sequence_no: Sequence number of the roster to delete.
        """
        try:
            context.database.remove_roster(int(sequence_no))
        except ValueError:
            raise InvalidArgumentError("sequence_no")

    @staticmethod
    def generate(context: Context, sequence_no: Union[int, str]) -> Roster:
        """
        Generate a roster.

        :param context: The context.
        :param sequence_no: Sequence number of the roster to generate.
        :return: The generated roster.
        """
        try:
            generator = Generator(context.database, Configuration())
            roster = generator.generate_roster(int(sequence_no))
            context.database.add_roster(roster)
            return roster
        except ValueError:
            raise InvalidArgumentError("sequence_no")

    @staticmethod
    def get(context: Context, sequence_no: Union[int, str]) -> Roster:
        """
        Get a roster.

        :param context: The context.
        :param sequence_no: Sequence number of the roster. Throws an exception if no roster with this sequence number
         is found.
        :return: The roster with the given sequence number.
        """
        try:
            return context.database.get_roster(int(sequence_no))
        except ValueError:
            raise InvalidArgumentError("sequence_no")

    @staticmethod
    def list(context: Context) -> list[Roster]:
        """
        Get the list of all rosters.

        :param context: The context.
        :return: List of rosters.
        """
        rosters = context.database.get_rosters()
        rosters.sort()
        return rosters
