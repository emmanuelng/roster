class ObjectNotFoundError(Exception):

    def __init__(self):
        super().__init__("Object not found.")
