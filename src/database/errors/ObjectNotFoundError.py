class ObjectNotFoundError(Exception):
    """
    Exception thrown when an object cannot be found.
    """

    def __init__(self):
        """
        Constructor.
        """
        super().__init__("Object not found.")
