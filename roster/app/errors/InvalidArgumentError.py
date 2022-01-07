class InvalidArgumentError(Exception):

    def __init__(self, argument_name: str):
        super().__init__(f"Invalid argument {argument_name}.")
