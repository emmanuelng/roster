import json
import os

from database.Dataclass import Dataclass
from database.drivers.ListDriver import ListDriver


class JsonDriver(ListDriver):
    """
    A driver that saves data in JSON files.
    """

    __data_classes_to_save: list[type]

    def __init__(self):
        """
        Constructor.
        """
        super(JsonDriver, self).__init__()
        self.__data_classes_to_save = []

    def __del__(self):
        """
        Destructor.
        """
        for data_class in self.__data_classes_to_save:
            self.__save_file(data_class)

    def clear_objects(self, data_class: type) -> None:
        super(JsonDriver, self).clear_objects(data_class)
        self.__set_dirty(data_class)

    def create_object(self, data_object: Dataclass) -> None:
        self.__load_file(data_object.__class__)
        super(JsonDriver, self).create_object(data_object)
        self.__set_dirty(data_object.__class__)

    def delete_objects(self, data_class: type, **kwargs) -> None:
        self.__load_file(data_class)
        super(JsonDriver, self).delete_objects(data_class, **kwargs)
        self.__set_dirty(data_class)

    def exists(self, data_class: type, **kwargs):
        self.__load_file(data_class)
        return super(JsonDriver, self).exists(data_class, **kwargs)

    def read_objects(self, data_class: type, **kwargs) -> list[Dataclass]:
        self.__load_file(data_class)
        return super(JsonDriver, self).read_objects(data_class, **kwargs)

    def update_object(self, data_object: Dataclass) -> None:
        self.__load_file(data_object.__class__)
        super(JsonDriver, self).update_object(data_object)
        self.__set_dirty(data_object.__class__)

    @staticmethod
    def __data_class_file_path(data_class: type) -> str:
        """
        Returns the path to the file containing the objects of the given data class.

        :param data_class: The data class.
        :return: File path.
        """
        return f"{data_class.__name__}.json"

    def __load_file(self, data_class: type) -> None:
        """
        Reads objects from the JSON files.

        :param data_class: Data class to load.
        :return:
        """
        # Check if it was already loaded.
        if data_class in self._objects:
            return

        # Check if the file exists.
        file_path = self.__data_class_file_path(data_class)
        if not os.path.isfile(file_path):
            return

        # Read the file
        self._objects[data_class] = []
        with open(file_path) as file:
            for data_object in json.load(file):
                self._objects[data_class] += [data_class(**data_object)]

    def __save_file(self, data_class: type) -> None:
        """
        Saves the objects in a JSON file.

        :param data_class: Data class to save.
        """
        if data_class not in self._objects:
            return

        file_path = self.__data_class_file_path(data_class)
        if not self._objects[data_class]:
            if os.path.exists(file_path):
                os.remove(file_path)
            return

        with open(file_path, "w") as file:
            object_dict_list = list(map(lambda d: d.to_dict(), self._objects[data_class]))
            json.dump(object_dict_list, file)

    def __set_dirty(self, data_class: type) -> None:
        """
        Indicates that a data class must be saved.

        :param data_class: The data class that needs to be saved.
        """
        if data_class not in self.__data_classes_to_save:
            self.__data_classes_to_save.append(data_class)
