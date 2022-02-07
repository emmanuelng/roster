class IncompleteKeyError(Exception):
    """
    Exception indicating that at least one element is missing in a data object key.
    """

    def __init__(self, missing_field: str):
        """
        Constructor.
        """
        super().__init__(f"The field '{missing_field}' is missing in the key.")
