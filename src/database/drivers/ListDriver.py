from database.Dataclass import Dataclass
from database.Driver import Driver


class ListDriver(Driver):
    """
    A driver that keeps its data in memory using python lists.
    """

    _objects: dict[type, list[Dataclass]]

    def __init__(self) -> None:
        """
        Constructor.
        """
        super().__init__()
        self._objects = {}

    def clear_objects(self, data_class: type) -> None:
        if data_class in self._objects:
            self._objects[data_class].clear()

    def create_object(self, data_object: Dataclass) -> None:
        if data_object.__class__ not in self._objects:
            self._objects[data_object.__class__] = [data_object]
        else:
            self._objects[data_object.__class__].append(data_object)

    def delete_objects(self, data_class: type, **kwargs) -> None:
        if data_class in self._objects:
            self._objects[data_class] = [o for o in self._objects[data_class] if not self.__is_selected(o, **kwargs)]

    def exists(self, data_class: type, **kwargs):
        return len(self.read_objects(data_class, **kwargs)) > 0

    def read_objects(self, data_class: type, **kwargs) -> list[Dataclass]:
        data_objects = self._objects.get(data_class, [])
        return list(filter(lambda o: self.__is_selected(o, **kwargs), data_objects))

    def update_object(self, data_object: Dataclass) -> None:
        self.delete_objects(data_object.__class__, **data_object.key())
        self.create_object(data_object)

    @staticmethod
    def __is_selected(data_object: Dataclass, **kwargs) -> bool:
        """
        Checks if an object is selected by the given search values.

        :param data_object: Data object to check.
        :param kwargs: Search values.
        :return: True if the object is selected, false otherwise.
        """
        for key, value in kwargs.items():
            if data_object.get(key) != value:
                return False
        return True
