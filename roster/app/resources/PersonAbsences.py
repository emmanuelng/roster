from app.Context import Context
from app.Resource import Resource, Action
from dataset.dataclasses.Absence import Absence


class PersonAbsences(Resource):

    def __init__(self) -> None:
        super().__init__()

        self._method("add", Action.CREATE, self.add)
        self._method("delete", Action.DELETE, self.delete)
        self._method("get", Action.GET, self.get)

    @staticmethod
    def add(context: Context, identifier, roster_sequence_no) -> None:
        """
        Add an absence.
        """
        person = context.dataset.get_person(identifier)
        context.dataset.add_absence(int(roster_sequence_no), person)

    @staticmethod
    def delete(context: Context, person_id: str, roster_sequence_no: str) -> None:
        """
        Remove an absence.
        """
        person = context.dataset.get_person(person_id)
        context.dataset.remove_absence(int(roster_sequence_no), person)

    @staticmethod
    def get(context: Context, person_id: str) -> list[Absence]:
        """
        Get the absences of a person.
        """
        person = context.dataset.get_person(person_id)
        return context.dataset.get_absences(person=person)
