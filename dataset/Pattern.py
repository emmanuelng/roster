from dataset.DataObject import DataObject


class Pattern(DataObject):

    def __init__(self, identifier: str) -> None:
        """
        Constructor.
        """
        super(Pattern, self).__init__()

        self.set_value("identifier", identifier)
        self.set_value("assignments", {})

    def __str__(self):
        assignments = self.assignments
        return "\n".join(map(lambda a: a[0] + ": " + str(a[1]), assignments.items()))

    @property
    def assignments(self) -> dict[str, int]:
        """
        Returns the assignments of the pattern.

        :return: The assignments as a dictionary (key: role, value: number of persons).
        """
        return self.get_value("assignments")

    @property
    def identifier(self) -> str:
        """
        Returns the identifier og the pattern.

        :return: Identifier of the pattern.
        """
        return self.get_value("identifier")

    @property
    def roles(self) -> list[str]:
        """
        Returns the list of roles of this pattern.

        :return: The list of role names.
        """
        return list(self.assignments.keys())

    def get_number(self, role: str) -> int:
        """
        Returns the number of person required for a role. If the pattern doesn't have the given role, returns 0.

        :param role: Requested role.
        :return: Number of persons required.
        """
        return self.assignments.get(role, 0)

    def set_assignment(self, role: str, number: int) -> None:
        """
        Sets an assignment.

        :param role: Role of the assignment.
        :param number: Number of persons required for this role.
        """
        assignments = self.assignments
        assignments[role] = number
        self.set_value("assignments", assignments)
