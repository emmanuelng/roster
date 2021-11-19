from typing import Optional

from configuration.Configuration import Configuration
from dataset.Dataset import Dataset
from dataset.Person import Person
from dataset.Roster import Roster
from generator.Evaluator import Evaluator
from generator.algorithms.SimpleAlgorithm import SimpleAlgorithm
from generator.algorithms.TreeAlgorithm import TreeAlgorithm
from generator.errors.UnknownAlgorithmError import UnknownAlgorithmError
from generator.evaluators.AlternateRolesEvaluator import AlternateRolesEvaluator
from generator.evaluators.MaximizeRestTimeEvaluator import MaximizeRestTimeEvaluator


class Generator:

    def __init__(self, dataset: Dataset, config: Configuration) -> None:
        """
        Constructor.
        :param dataset: The data used to access the dataset.
        :param config: Configuration of the generator.
        """
        self._dataset = dataset
        self._config = config

        self._evaluators = {
            "alternate_roles": AlternateRolesEvaluator(dataset),
            "maximize_rest_time": MaximizeRestTimeEvaluator(dataset)
        }

        self._algorithms = {
            "simple": SimpleAlgorithm(self),
            "tree": TreeAlgorithm(self)
        }

    @property
    def configuration(self) -> Configuration:
        """
        Configuration of this generator.
        """
        return self._config

    @property
    def dataset(self) -> Dataset:
        """
        Dataset used by this generator.
        """
        return self._dataset

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
         the other rosters in the dataset set. For example, the roster with sequence number 1 is considered to be before
         roster 2.
        :return: A roster.
        """
        algorithm_name = self._config.get("algorithm", "tree")
        if algorithm_name not in self._algorithms:
            raise UnknownAlgorithmError()

        return self._algorithms[algorithm_name].generate_roster(sequence_no)
