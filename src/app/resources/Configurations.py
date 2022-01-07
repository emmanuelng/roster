from app.Resource import Resource, Action
from configuration.Configuration import Configuration


class Configurations(Resource):

    def __init__(self) -> None:
        super().__init__()

        # Methods
        self._method("get", Action.GET, self.get)
        self._method("list", Action.GET, self.list)
        self._method("set", Action.UPDATE, self.set)

    @staticmethod
    def get(key):
        """
        Get the value of a configuration variable.
        """
        return Configuration().get(key)

    @staticmethod
    def list():
        """
        Get the values of the configuration variables.
        """
        return Configuration().values

    @staticmethod
    def set(key, value):
        """
        Set the value of a configuration variable.
        """
        Configuration().set(key, value)
