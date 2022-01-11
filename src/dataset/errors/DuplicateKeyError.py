class DuplicateKeyError(Exception):

    def __init__(self):
        super().__init__("An object with the same key already exists.")
