import dataclasses

from app.Context import Context
from app.Resource import Resource, Action
from app.errors.InvalidArgumentError import InvalidArgumentError


class PersonRoles(Resource):

    def __init__(self) -> None:
        """
        Constructor.
        """
        super().__init__()

        # Methods
        self._method("add", Action.UPDATE, self.add)
        self._method("get", Action.GET, self.get)
        self._method("remove", Action.DELETE, self.remove)

    @staticmethod
    def add(context: Context, person_id: str, role: str) -> None:
        """
        Add a role to a person.

        :param context: The context.
        :param person_id: Identifier of the person.
        :param role: New role.
        """
        if not role:
            raise InvalidArgumentError("role")

        person = context.database.get_person(person_id)
        if person is None or person.has_role(role):
            return

        context.database.remove_person(person_id)
        context.database.add_person(dataclasses.replace(person, roles=person.roles + [role]))

    @staticmethod
    def get(context: Context, person_id: str) -> list[str]:
        """
        Get the roles of a person.

        :param context: The context.
        :param person_id: Identifier of the person.
        :return: A list of roles.
        """
        roles = context.database.get_person(person_id).roles
        roles.sort()
        return roles

    @staticmethod
    def remove(context: Context, person_id: str, role: str) -> None:
        """
        Remove a role to a person.

        :param context: The context.
        :param person_id: Identifier of the person.
        :param role: Role to remove.
        """
        if not role:
            raise InvalidArgumentError("role")

        person = context.database.get_person(person_id)
        if person is None or not person.has_role(role):
            return

        context.database.remove_person(person_id)
        context.database.add_person(dataclasses.replace(person, roles=list(filter(lambda r: r != role, person.roles))))
