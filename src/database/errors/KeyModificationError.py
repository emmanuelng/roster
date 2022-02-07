class KeyModificationError(Exception):
    """
    Exception thrown when a modification changes the key of a data object.
    """

    def __init__(self, modified_fields: list[str]):
        """
        Constructor.

        :param modified_fields:
        """
        if len(modified_fields) == 1:
            super().__init__(f"You cannot modify the field '{modified_fields[0]}' as it is part of the key of the "
                             f"object.")
        elif len(modified_fields > 1):
            modified_fields_str = ", ".join(map(lambda f: f"'{f}'", modified_fields))
            super().__init__(f"You cannot modify the fields {modified_fields_str} as they are part of the key of the "
                             f"object.")
        else:
            super().__init__(f"You cannot modify the key of the object.")
