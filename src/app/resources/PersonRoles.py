import dataclasses

from app.Context import Context
from app.Resource import Resource, Action


class PersonRoles(Resource):

    def __init__(self) -> None:
        super().__init__()

        # Methods
        self._method("add", Action.UPDATE, self.add)
        self._method("get", Action.GET, self.get)

    @staticmethod
    def add(context: Context, person_id: str, role: str) -> None:
        """
        Add a role to a person.
        """
        person = context.database.get_person(person_id)
        if person is None or person.has_role(role):
            return

        context.database.remove_person(person_id)
        context.database.add_person(dataclasses.replace(person, roles=person.roles + [role]))

    @staticmethod
    def get(context: Context, person_id: str) -> list[str]:
        """
        Get the roles of a person.
        """
        return context.database.get_person(person_id).roles
