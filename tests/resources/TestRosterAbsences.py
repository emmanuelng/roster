from TestCase import TestCase
from app.errors.InvalidArgumentError import InvalidArgumentError
from app.resources.Persons import Persons
from app.resources.RosterAbsences import RosterAbsences
from app.resources.Rosters import Rosters
from database.errors.ObjectNotFoundError import ObjectNotFoundError


class TestRosterAbsences(TestCase):

    def test_create_success(self):
        """
        Tests that it is possible to create an absence.
        """
        # Add a person and a roster.
        Persons.create(self.context, "id", "f_name", "l_name")
        Rosters.create(self.context, "123")

        # Add an absence.
        absence = RosterAbsences.create(self.context, "123", "id")

        # Check that the absence was correctly initialized.
        self.assertEqual(123, absence.roster_sequence_no)
        self.assertEqual("id", absence.person_identifier)

        # Check that the absence was added.
        self.assertIn(absence, RosterAbsences.list(self.context, "123"))

    def test_create_success_unknown_roster(self):
        """
        Tests that it is possible to define absences for rosters that don't exist yet.
        """
        Persons.create(self.context, "id", "f_name", "l_name")
        absence = RosterAbsences.create(self.context, "123", "id")
        self.assertIn(absence, RosterAbsences.list(self.context, "123"))

    def test_create_error_invalid_roster_sequence_no(self):
        """
        Tests that invalid roster sequence numbers are rejected.
        """
        Persons.create(self.context, "id", "f_name", "l_name")

        # Non numeric value.
        with self.assertRaises(InvalidArgumentError):
            RosterAbsences.create(self.context, "abc", "id")

        # Empty value.
        with self.assertRaises(InvalidArgumentError):
            RosterAbsences.create(self.context, "", "id")

    def test_create_error_unknown_person(self):
        """
        Tests that an exception is raised when the person doesn't exist.
        """
        Rosters.create(self.context, "123")
        with self.assertRaises(ObjectNotFoundError):
            RosterAbsences.create(self.context, "123", "id")

    def test_delete_success(self):
        """
        Tests that it is possible to delete an absence.
        """
        # Add two person.
        Persons.create(self.context, "person1", "f_name", "l_name")
        Persons.create(self.context, "person2", "f_name", "l_name")

        # Add absences.
        absence1 = RosterAbsences.create(self.context, "123", "person1")
        absence2 = RosterAbsences.create(self.context, "123", "person2")
        self.assertEqual([absence1, absence2], RosterAbsences.list(self.context, "123"))

        # Delete one absence.
        RosterAbsences.delete(self.context, "123", "person1")
        self.assertEqual([absence2], RosterAbsences.list(self.context, "123"))

    def test_delete_success_unknown_roster(self):
        """
        Tests that attempting to delete an unknown absence doesn't raise any exception.
        """
        Persons.create(self.context, "id", "f_name", "l_name")
        RosterAbsences.delete(self.context, "123", "id")

    def test_delete_error_unknown_person(self):
        """
        Tests that an exception is raised when the person doesn't exist.
        """
        Rosters.create(self.context, "123")
        with self.assertRaises(ObjectNotFoundError):
            RosterAbsences.delete(self.context, "123", "xyz")

    def test_list_success(self):
        """
        Tests that it is possible to get the absences of a person.
        """
        # Add two persons.
        Persons.create(self.context, "person1", "bbb", "bbb")
        Persons.create(self.context, "person2", "aaa", "aaa")

        # Add two absences.
        absence1 = RosterAbsences.create(self.context, "123", "person1")
        absence2 = RosterAbsences.create(self.context, "123", "person2")

        # Check that the absences are sorted by person names.
        self.assertEqual([absence2, absence1], RosterAbsences.list(self.context, "123"))
