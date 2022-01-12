from TestCase import TestCase
from app.errors.InvalidArgumentError import InvalidArgumentError
from app.resources.PersonAbsences import PersonAbsences
from app.resources.Persons import Persons
from app.resources.Rosters import Rosters
from database.errors.ObjectNotFoundError import ObjectNotFoundError


class TestPersonAbsences(TestCase):

    def test_create_success(self):
        """
        Tests that it is possible to create an absence.
        """
        # Add a person and a roster.
        Persons.create(self.context, "id", "f_name", "l_name")
        Rosters.create(self.context, "123")

        # Add an absence.
        absence = PersonAbsences.create(self.context, "id", "123")

        # Check that the absence was correctly initialized.
        self.assertEqual("id", absence.person_identifier)
        self.assertEqual(123, absence.roster_sequence_no)

        # Check that the absence was added.
        self.assertIn(absence, PersonAbsences.list(self.context, "id"))

    def test_create_success_unknown_roster(self):
        """
        Tests that it is possible to define absences for rosters that don't exist yet.
        """
        Persons.create(self.context, "id", "f_name", "l_name")
        absence = PersonAbsences.create(self.context, "id", "123")
        self.assertIn(absence, PersonAbsences.list(self.context, "id"))

    def test_create_error_invalid_roster_sequence_no(self):
        """
        Tests that invalid roster sequence numbers are rejected.
        """
        Persons.create(self.context, "id", "f_name", "l_name")

        # Non numeric value.
        with self.assertRaises(InvalidArgumentError):
            PersonAbsences.create(self.context, "id", "abc")

        # Empty value.
        with self.assertRaises(InvalidArgumentError):
            PersonAbsences.create(self.context, "id", "")

    def test_create_error_unknown_person(self):
        """
        Tests that an exception is raised when the person doesn't exist.
        """
        Rosters.create(self.context, "123")
        with self.assertRaises(ObjectNotFoundError):
            PersonAbsences.create(self.context, "id", "123")

    def test_delete_success(self):
        """
        Tests that it is possible to delete an absence.
        """
        # Add a person.
        Persons.create(self.context, "id", "f_name", "l_name")

        # Add two absences.
        absence1 = PersonAbsences.create(self.context, "id", "123")
        absence2 = PersonAbsences.create(self.context, "id", "456")
        self.assertEqual([absence1, absence2], PersonAbsences.list(self.context, "id"))

        # Delete one absence.
        PersonAbsences.delete(self.context, "id", "123")
        self.assertEqual([absence2], PersonAbsences.list(self.context, "id"))

    def test_delete_success_unknown_roster(self):
        """
        Tests that attempting to delete an unknown absence doesn't raise any exception.
        """
        Persons.create(self.context, "id", "f_name", "l_name")
        PersonAbsences.delete(self.context, "id", "123")

    def test_delete_error_unknown_person(self):
        """
        Tests that an exception is raised when the person doesn't exist.
        """
        Rosters.create(self.context, "123")
        with self.assertRaises(ObjectNotFoundError):
            PersonAbsences.delete(self.context, "xyz", "123")

    def test_list_success(self):
        """
        Tests that it is possible to get the absences of a person.
        """
        # Add a person.
        Persons.create(self.context, "id", "f_name", "l_name")

        # Add two absences.
        absence1 = PersonAbsences.create(self.context, "id", "456")
        absence2 = PersonAbsences.create(self.context, "id", "123")

        # Check that the absences are sorted by roster sequence number.
        self.assertEqual([absence2, absence1], PersonAbsences.list(self.context, "id"))
