import unittest
from abc import ABC

from app.Context import Context
from database.databases.ListDatabase import ListDatabase


class TestCase(ABC, unittest.TestCase):
    """
    Base test case.
    """

    __context: Context

    def __init__(self, method_name='runTest'):
        """
        Constructor.

        :param method_name: Name of the test to execute.
        """
        super().__init__(method_name)
        self.__context = Context(ListDatabase())

    @property
    def context(self) -> Context:
        """
        Test context.
        """
        return self.__context
