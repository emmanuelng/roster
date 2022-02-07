import sys

from app.App import App
from app.errors.MethodNotFoundError import MethodNotFoundError
from app.resources.Configurations import Configurations
from database.Database import Database
from database.drivers.JsonDriver import JsonDriver


class ConsoleApp(App):
    """
    Command-line application.
    """

    def __init__(self):
        super().__init__(Database(driver=JsonDriver()))

        # Resources
        self._resource("config", Configurations())

    def start(self) -> None:
        try:
            command_path = sys.argv[1].split("-")
            command_args = sys.argv[2:]
            print(str(self.execute_method(command_path, *command_args)))
        except IndexError:
            print("Error: Missing command.")
            exit(1)
        except MethodNotFoundError:
            print("Error: Command not found.")
            exit(1)
        except Exception as e:
            print(f"Error: {str(e)}")
            exit(1)
