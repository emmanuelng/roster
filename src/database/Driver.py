from abc import ABC, abstractmethod

from database.Dataclass import Dataclass


class Driver(ABC):

    @abstractmethod
    def clear_objects(self, data_class: type) -> None:
        pass

    @abstractmethod
    def create_object(self, data_object: Dataclass) -> None:
        pass

    @abstractmethod
    def delete_objects(self, data_class: type, key: dict[str, any]) -> None:
        pass

    @abstractmethod
    def exists(self, data_class: type, **kwargs):
        pass

    @abstractmethod
    def read_objects(self, data_class: type, **kwargs) -> list[Dataclass]:
        pass

    @abstractmethod
    def update_object(self, data_object: Dataclass) -> None:
        pass
