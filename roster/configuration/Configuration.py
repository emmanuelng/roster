import json
import os


class Configuration:

    def __init__(self, path="./roster_config.json"):
        """
        Constructor.
        """
        self._path = path
        self._values = {}
        self._read_config_file()

    @property
    def values(self):
        return self._values

    def get(self, key: str, default: any = None) -> any:
        """
        Gets a configuration variable.

        :param key: Name of the variable.
        :param default: Default value.
        :return: The value.
        """
        return self._values.get(key, default)

    def set(self, key: str, value: any) -> None:
        """
        Sets a configuration variable.

        :param key: Name of the variable.
        :param value: Value of the variable.
        """
        self._values[key] = value
        self._write_config_file()

    def _read_config_file(self) -> None:
        """
        Reads the configuration file if it exists.
        """
        # noinspection PyBroadException
        try:
            if os.path.isfile(self._path):
                file = open(self._path)
                self._values = json.loads(file.read())
                file.close()
        except:
            return

    def _write_config_file(self) -> None:
        """
        Writes the currents in a configuration file.
        """
        file = open(self._path, "w")
        file.write(json.dumps(self._values, indent=4, sort_keys=True))
        file.close()
