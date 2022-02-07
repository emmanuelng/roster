from inspect import isclass


class InvalidDataclassError(Exception):
    """
    Exception indicating that a data class is not valid, either because it is not supported by a database, or because it
    isn't a subclass of the Dataclass class.
    """

    def __init__(self, data_class: type):
        """
        Constructor.

        :param data_class: The invalid data class.
        """
        if isclass(data_class):
            super().__init__(f"The dataclass '{data_class.__name__}' is not supported by the database.")
        else:
            super().__init__(f"'{data_class}' is not a data class.")
