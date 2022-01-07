import dataclasses

from app.Context import Context
from app.Resource import Resource, Action


class Roles(Resource):

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
        person = context.dataset.get_person(person_id)
        if person is None or person.has_role(role):
            return

        context.dataset.remove_person(person_id)
        context.dataset.add_person(dataclasses.replace(person, roles=person.roles + [role]))

    @staticmethod
    def get(context: Context, person_id: str) -> list[str]:
        """
        Get the roles of a person.
        """
        return context.dataset.get_person(person_id).roles
