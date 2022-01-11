import unittest
from abc import ABC

from app.Context import Context
from dataset.Dataset import Dataset
from dataset.datasets.ListDataset import ListDataset


class TestCase(ABC, unittest.TestCase):
    """
    Base test case.
    """

    __dataset: Dataset
    __context: Context

    def __init__(self, method_name='runTest'):
        """
        Constructor.

        :param method_name: Name of the test to execute.
        """
        super().__init__(method_name)

        self.__dataset = ListDataset()
        self.__context = Context(self.__dataset)

    @property
    def dataset(self) -> Dataset:
        """
        Instance of the dataset used by the tests.
        """
        return self.__dataset

    @property
    def context(self) -> Context:
        """
        Test context.
        """
        return self.__context
