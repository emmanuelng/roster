import unittest
from abc import ABC

from app.Context import Context
from database.Database import Database
from database.drivers.ListDriver import ListDriver


class TestCase(ABC, unittest.TestCase):
    """
    Base test case.
    """

    __database: Database
    __context: Context

    def __init__(self, method_name='runTest'):
        """
        Constructor.

        :param method_name: Name of the test to execute.
        """
        super().__init__(method_name)
        self.__database = Database(driver=ListDriver())
        self.__context = Context(self.__database)
        self.__database.clear()

    def __del__(self):
        """
        Destructor.
        """
        self.__database.clear()

    @property
    def context(self) -> Context:
        """
        Test context.
        """
        return self.__context
