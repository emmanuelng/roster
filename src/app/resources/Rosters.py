from app.Context import Context
from app.Resource import Resource, Action
from app.resources.Assignments import Assignments
from configuration.Configuration import Configuration
from database.dataclasses.Roster import Roster
from generator.Generator import Generator


class Rosters(Resource):

    def __init__(self) -> None:
        super().__init__()

        # Child resources
        self._child_resource("assignments", Assignments())

        # Methods
        self._method("create", Action.CREATE, self.create)
        self._method("delete", Action.DELETE, self.delete)
        self._method("test", Action.CREATE, self.generate)
        self._method("generate", Action.CREATE, self.generate_and_save)
        self._method("get", Action.GET, self.get)
        self._method("list", Action.GET, self.list)

    @staticmethod
    def create(context: Context, sequence_no: str) -> None:
        """
        Create a new roster.
        """
        context.database.add_roster(Roster(sequence_no))

    @staticmethod
    def delete(context: Context, sequence_no: str) -> None:
        """
        Remove a roster.
        """
        context.database.remove_roster(int(sequence_no))

    @staticmethod
    def generate(context: Context, sequence_no: str) -> Roster:
        """
        Generate a roster.
        """
        generator = Generator(context.database, Configuration())
        generated_roster = generator.generate_roster(int(sequence_no))

        if generated_roster is None:
            raise Exception("Could not generate a roster.")

        return generated_roster

    @staticmethod
    def generate_and_save(context: Context, sequence_no: str) -> Roster:
        """
        Generate and save a roster.
        """
        roster = Rosters.generate(context, sequence_no)
        context.database.add_roster(roster)
        return roster

    @staticmethod
    def get(context: Context, sequence_no: str) -> list[Roster]:
        """
        Display the details of a specific roster.
        """
        return context.database.get_roster(int(sequence_no))

    @staticmethod
    def list(context: Context) -> list[Roster]:
        """
        Display the list of all rosters.
        """
        return context.database.get_rosters()
