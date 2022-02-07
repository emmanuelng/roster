from typing import Optional

from database.Dataclass import Dataclass, Schema
from database.Driver import Driver
from database.dataclass.Absence import Absence
from database.dataclass.Pattern import Pattern
from database.dataclass.Person import Person
from database.dataclass.Roster import Roster
from database.drivers.ListDriver import ListDriver
from database.errors.DuplicateKeyError import DuplicateKeyError
from database.errors.IncompleteKeyError import IncompleteKeyError
from database.errors.InvalidDataclassError import InvalidDataclassError
from database.errors.KeyModificationError import KeyModificationError
from database.errors.ObjectNotFoundError import ObjectNotFoundError


class Database:
    """
    Database class. A database manages data classes. A driver allows the database to interact with the system.
    """

    __driver: Driver
    __data_classes: list[type]

    def __init__(self, driver: Driver = None):
        """
        Constructor.

        :param driver: The driver to use.
        """
        self.__driver = driver if driver else ListDriver()
        self.__data_classes = []

        # Register default dataclasses.
        self._dataclass(Absence)
        self._dataclass(Pattern)
        self._dataclass(Person)
        self._dataclass(Roster)

    def create(self, data_class: type, **kwargs) -> Dataclass:
        """
        Creates a new data object.

        :param data_class: Class of the object.
        :param kwargs: Initial values of the object.
        :return: The newly created object.
        """
        if data_class not in self.__data_classes:
            raise InvalidDataclassError(data_class)

        data_object = data_class(**kwargs)
        if self.__driver.exists(data_class, **data_object.key()):
            raise DuplicateKeyError()

        self.__driver.create_object(data_object)
        return data_object

    def clear(self, data_class: Optional[type] = None) -> None:
        """
        Clears objects.

        :param data_class: The class of objects to clear. If None, clears the entire database.
        """
        if data_class is None:
            for current_data_class in self.__data_classes:
                self.__driver.clear_objects(current_data_class)
            return

        if data_class not in self.__data_classes:
            raise InvalidDataclassError(data_class)

        self.__driver.clear_objects(data_class)

    def delete(self, data_class: type, **kwargs) -> None:
        """
        Deletes data objects.

        :param data_class: The class of objects to delete.
        :param kwargs: Search values. Objects having all the given values will be deleted.
        """
        if data_class not in self.__data_classes:
            raise InvalidDataclassError(data_class)
        else:
            self.__driver.delete_objects(data_class, **kwargs)

    def get(self, data_class: type, **kwargs) -> list[Dataclass]:
        """
        Gets data objects.

        :param data_class: The class of objects to get.
        :param kwargs: Search values. Objects having all the given values will be returned.
        :return: List of data objects corresponding to the given search values.
        """
        if data_class not in self.__data_classes:
            raise InvalidDataclassError(data_class)
        else:
            objects = self.__driver.read_objects(data_class, **kwargs)
            return objects

    def get_unique(self, data_class: type, **kwargs) -> Dataclass:
        """
        Gets a unique data object.

        :param data_class: The class of the object.
        :param kwargs: Key values. All elements of the key of the desired object must be provided.
        :return: The object.
        """
        if data_class not in self.__data_classes:
            raise InvalidDataclassError(data_class)

        for field_name in Schema(data_class).key_fields.keys():
            if field_name not in kwargs:
                raise IncompleteKeyError(field_name)

        objects = self.__driver.read_objects(data_class, **kwargs)
        if not objects:
            raise ObjectNotFoundError()

        return objects[0]

    def update(self, data_object: Dataclass, **kwargs) -> Dataclass:
        """
        Updates a data object.

        :param data_object: Data object to modify.
        :param kwargs: New values.
        :return: An copy of the given data object with the new values.
        """
        if data_object.__class__ not in self.__data_classes:
            raise InvalidDataclassError(data_object.__class__)

        updated_data_object = data_object.replace(**kwargs)
        if data_object.key() != updated_data_object.key():
            diff = list(dict(set(data_object.key().items()) ^ set(updated_data_object.key().items())).keys())
            raise KeyModificationError(diff)

        self.__driver.update_object(updated_data_object)
        return updated_data_object

    def _dataclass(self, dataclass: type) -> None:
        """
        Registers a data class.

        :param dataclass: Data class to register.
        """
        if not issubclass(dataclass, Dataclass):
            raise Exception()

        if dataclass not in self.__data_classes:
            self.__data_classes.append(dataclass)
