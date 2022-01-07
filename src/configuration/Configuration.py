import json
import os


class Configuration:
    """
    Configuration class.
    """

    __path: str
    __values: dict[str, any]

    def __init__(self, path: str = "./roster_config.json"):
        """
        Constructor.
        """
        self.__path = path
        self.__values = {}

        self.__read_config_file()

    def __str__(self):
        return str(self.values)

    @property
    def values(self) -> dict[str, any]:
        """
        Configuration values.
        """
        return self.__values

    def get(self, key: str, default: any = None) -> any:
        """
        Gets a configuration variable.

        :param key: Name of the variable.
        :param default: Default value.
        :return: The value.
        """
        return self.__values.get(key, default)

    def set(self, key: str, value: any) -> None:
        """
        Sets a configuration variable.

        :param key: Name of the variable.
        :param value: Value of the variable.
        """
        self.__values[key] = value
        self.__write_config_file()

    def __read_config_file(self) -> None:
        """
        Reads the configuration file if it exists.
        """
        # noinspection PyBroadException
        try:
            if os.path.isfile(self.__path):
                file = open(self.__path)
                self.__values = json.loads(file.read())
                file.close()
        except:
            return

    def __write_config_file(self) -> None:
        """
        Writes the currents in a configuration file.
        """
        file = open(self.__path, "w")
        file.write(json.dumps(self.__values, indent=4, sort_keys=True))
        file.close()
