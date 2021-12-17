from abc import ABC


class Object(ABC):

    def __init__(self) -> None:
        """
        Constructor.
        """
        self._values = {}
        self._on_modify = []

    def get_value(self, name: str) -> any:
        """
        Returns a value of the object.

        :param name: Name of the value.
        :return: The value.
        """
        return self._values[name] if name in self._values else None

    def set_value(self, name: str, value: any) -> None:
        """
        Sets a value of the object.

        :param name: Name of the value.
        :param value: The value.
        """
        self._values[name] = value
