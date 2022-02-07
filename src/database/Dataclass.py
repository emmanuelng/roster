from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from inspect import isclass
from typing import Optional

from database.errors.InvalidDataclassError import InvalidDataclassError


class Dataclass:
    """
    Represents a data class, i.e. a type of objects managed by the database. Instances of this class represent objects
    of this type. A data class object is immutable. It is however possible to created modified copies with the replace()
    method.
    """

    __schema: Schema
    __values: dict[str, any]

    def __init__(self, **kwargs) -> None:
        """
        Constructor.

        :param kwargs: Initial values.
        """
        self.__schema = Schema(self.__class__)

        # Initialize all fields to None.
        fields = self.__schema.fields
        self.__values = {field_name: None for field_name, field in fields.items()}

        # Set values in kwargs.
        for key, value in kwargs.items():
            if key not in self.__values:
                dataclass_name = self.__class__.__name__
                raise AttributeError(f"'{dataclass_name}' dataclass has no field '{key}'")
            self.__values[key] = value

        # Set default values
        for name, field in fields.items():
            if name in kwargs:
                continue

            if field.default is not None:
                self.__values[name] = field.default
            elif field.default_factory:
                self.__values[name] = field.default_factory()

    def __str__(self):
        return str(self.__values)

    def __hash__(self):
        return hash(self.key().values())

    def __getattribute__(self, item):
        # Non-public attributes or methods
        if item.startswith("_"):
            return super(Dataclass, self).__getattribute__(item)

        try:
            # Methods or public attributes that are not fields.
            attribute = super(Dataclass, self).__getattribute__(item)
            if callable(attribute) or item not in self.__values:
                return attribute
        except AttributeError as e:
            # Ignore attribute errors if it is a field.
            if item not in self.__values:
                raise e

        # Get field value.
        return self.get(item)

    def get(self, field: str) -> any:
        """
        Gets the value of a field.

        :param field: Name of the field.
        :return: The value of the field.
        """
        if field not in self.__values:
            dataclass_name = self.__class__.__name__
            raise AttributeError(f"'{dataclass_name}' dataclass has no field '{field}'")
        return self.__values.get(field, None)

    def key(self) -> dict[str, any]:
        """
        Returns the field values of this data class object.
        :return: A dictionary. The keys are the names of the fields, associated with their values.
        """
        return {key: self.get(key) for key, field in self.__schema.key_fields.items()}

    def replace(self, **kwargs):
        """
        Create a modified copy of a data class object.
        :param kwargs: The modified values.
        :return: A modified copy of this object.
        """
        copy_obj = deepcopy(self)

        for key, value in kwargs.items():
            if key not in copy_obj.__values:
                raise AttributeError(f"'{copy_obj.__class__}' dataclass has no field '{key}'")
            copy_obj.__values[key] = value

        return copy_obj

    def to_dict(self) -> dict[str, any]:
        """
        Converts the data class object to a python dictionary.
        :return:
        """
        return self.__values.copy()


@dataclass(frozen=True)
class Field:
    """
    Represents a field of a data class.
    """

    key: bool = True
    default: Optional[any] = None
    default_factory: Optional[callable] = None


class Schema:
    """
    Represents the schema of a data class.
    """

    __fields: dict[str, Field]

    def __init__(self, data_class: type):
        """
        Constructor.

        :param data_class: Data class.
        """
        if not isclass(data_class) or not issubclass(data_class, Dataclass):
            raise InvalidDataclassError(data_class)

        all_members = set(dir(data_class) + list(data_class.__annotations__.keys()))
        public_members = filter(lambda m: not m.startswith("_"), all_members)

        self.__fields = {}
        for member in public_members:
            value = getattr(data_class, member, None)
            if value is None or isinstance(value, Field):
                self.__fields[member] = value if isinstance(value, Field) else Field()

    @property
    def fields(self) -> dict[str, Field]:
        """
        Fields of the data class.
        """
        return self.__fields

    @property
    def key_fields(self) -> dict[str, Field]:
        """
        Key fields of the data class.
        """
        return {name: field for name, field in self.__fields.items() if field.key}
