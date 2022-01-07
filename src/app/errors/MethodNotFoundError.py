class MethodNotFoundError(Exception):

    def __init__(self):
        super().__init__("Method not found.")
