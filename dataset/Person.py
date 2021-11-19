from dataset.DataObject import DataObject


class Person(DataObject):

    def __init__(self, identifier: str, first_name: str, last_name: str, roles: list[str] = None) -> None:
        """
        Constructor.
        :param identifier: Person identifier.
        :param first_name: First name of the person.
        :param last_name: Last name of the person.
        :param roles: Roles of the person.
        """
        super(Person, self).__init__()

        self.set_value("identifier", identifier)
        self.set_value("first_name", first_name)
        self.set_value("last_name", last_name)
        self.set_value("roles", list(set(roles)) if (roles is not None) else [])

    def __eq__(self, other):
        return isinstance(other, Person) and self.identifier == other.identifier

    def __hash__(self):
        return hash(self.identifier)

    def __str__(self) -> str:
        return self.first_name + ' ' + self.last_name

    @property
    def identifier(self) -> str:
        """
        Returns the identifier of the person.

        :return: The identifier.
        """
        return self.get_value("identifier")

    @property
    def first_name(self) -> str:
        """
        Returns the first name of the person.

        :return: The first name.
        """
        return self.get_value("first_name")

    @property
    def full_name(self) -> str:
        """
        Returns the full name of the person.

        :return: A string with the full name of the person.
        """
        return self.first_name + " " + self.last_name

    @property
    def last_name(self) -> str:
        """
        Returns the last name of the person.

        :return: The last name.
        """
        return self.get_value("last_name")

    @property
    def roles(self) -> list[str]:
        """
        Returns the list of roles of this person.

        :return: A list of role names.
        """
        return self.get_value("roles")

    def add_role(self, role: str) -> None:
        """
        Adds a role to this person.

        :param role: The role to add.
        """
        roles = self.roles
        roles += [role]
        self.set_value("roles", list(set(roles)))

    def has_role(self, role: str) -> bool:
        """
        Checks if this person has a role.

        :param role: The role
        :return: True if the person has the role, false otherwise.
        """
        return role in self.roles
