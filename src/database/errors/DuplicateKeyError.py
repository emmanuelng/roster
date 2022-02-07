class DuplicateKeyError(Exception):
    """
    Exception thrown when the user tries to create an object with the same key as an existing one (e.g. object with the
    same identifier.)
    """

    def __init__(self):
        """
        Constructor.
        """
        super().__init__("An object with the same field already exists.")
