from typing import Optional

from configuration.Configuration import Configuration
from database.Database import Database
from database.dataclass.Roster import Roster
from generator.Evaluator import Evaluator
from generator.algorithms.SimpleAlgorithm import SimpleAlgorithm
from generator.algorithms.TreeAlgorithm import TreeAlgorithm
from generator.errors.UnknownAlgorithmError import UnknownAlgorithmError
from generator.evaluators.AlternateRolesEvaluator import AlternateRolesEvaluator
from generator.evaluators.MaximizeRestTimeEvaluator import MaximizeRestTimeEvaluator


class Generator:
    """
    Roster generator.
    """

    __database: Database
    __config: Configuration

    def __init__(self, database: Database, config: Configuration) -> None:
        """
        Constructor.
        :param database: The data used to access the database.
        :param config: Configuration of the generator.
        """
        self.__database = database
        self.__config = config

        self._evaluators = {
            "alternate_roles": AlternateRolesEvaluator(database),
            "maximize_rest_time": MaximizeRestTimeEvaluator(database)
        }

        self._algorithms = {
            "simple": SimpleAlgorithm(self),
            "tree_fast": TreeAlgorithm(self, quality="low"),
            "tree_medium": TreeAlgorithm(self, quality="medium"),
            "tree_slow": TreeAlgorithm(self, quality="high")
        }

    @property
    def configuration(self) -> Configuration:
        """
        Configuration of this generator.
        """
        return self.__config

    @property
    def database(self) -> Database:
        """
        Database used by this generator.
        """
        return self.__database

    @property
    def evaluators(self) -> list[Evaluator]:
        """
        List of assignments evaluators of this generator.
        """
        return self._evaluators

    def generate_roster(self, sequence_no: int) -> Optional[Roster]:
        """
        Generates a roster.

        :param sequence_no: Sequence number of the roster. This number indicates the chronological order in relation to
         the other rosters in the database set. For example, the roster with sequence number 1 is considered to be
         before roster 2.
        :return: A roster.
        """
        algorithm_name = self.__config.get("algorithm", "tree_fast")
        if algorithm_name not in self._algorithms:
            raise UnknownAlgorithmError()

        return self._algorithms[algorithm_name].generate_roster(sequence_no)
