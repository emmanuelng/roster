from dataclasses import dataclass

from database.Database import Database


@dataclass(frozen=True)
class Context:
    """
    Class representing the context in which a command is invoked.
    """

    database: Database
