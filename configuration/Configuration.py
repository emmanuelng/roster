import json
import os


class Configuration:

    def __init__(self):
        """
        Constructor.
        """
        self._values = {}
        self._read_config_file()

    def get(self, key: str, default: any = None) -> any:
        """
        Gets a value from the properties.

        :param key: Name of the property.
        :param default: Default value.
        :return: The value.
        """
        return self._values.get(key, default)

    def _read_config_file(self) -> None:
        """
        Reads the configuration file if it exists.
        """
        # noinspection PyBroadException
        try:
            file_path = "roster_config.json"
            if os.path.isfile(file_path):
                file = open(file_path)
                self._values = json.loads(file.read())
        except:
            return
