from abc import ABC
from typing import Callable


class DataObject(ABC):

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
        modified = name in self._values
        self._values[name] = value

        if not modified:
            return

        for callback in self._on_modify:
            callback()

    def on_modify(self, callback: Callable[[str, any, any], None]) -> None:
        """
        Registers a callback to call when this object is modified.

        :param callback: The callback function.
        """
        self._on_modify.append(callback)
