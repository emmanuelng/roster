from dataclasses import dataclass

from dataset.Dataset import Dataset


@dataclass(frozen=True)
class Context:
    """
    Class representing the context in which a command is invoked.
    """

    dataset: Dataset
