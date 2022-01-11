import unittest
from abc import ABC

from app.Context import Context
from database.Database import Database
from database.databases.ListDatabase import ListDatabase


class TestCase(ABC, unittest.TestCase):
    """
    Base test case.
    """

    __dataset: Database
    __context: Context

    def __init__(self, method_name='runTest'):
        """
        Constructor.

        :param method_name: Name of the test to execute.
        """
        super().__init__(method_name)

        self.__dataset = ListDatabase()
        self.__context = Context(self.__dataset)

    @property
    def database(self) -> Database:
        """
        Instance of the database used by the tests.
        """
        return self.__dataset

    @property
    def context(self) -> Context:
        """
        Test context.
        """
        return self.__context
