from TestCase import TestCase
from app.errors.InvalidArgumentError import InvalidArgumentError
from app.resources.Persons import Persons
from app.resources.RosterAssignments import RosterAssignments
from app.resources.Rosters import Rosters
from database.errors.ObjectNotFoundError import ObjectNotFoundError


class TestRosterAssignments(TestCase):

    def test_create_success(self) -> None:
        """
        Tests that it is possible to assign a person in a roster.
        """
        roster = Rosters.create(self.context, "123")
        person1 = Persons.create(self.context, "id1", "abc", "def")
        person2 = Persons.create(self.context, "id2", "abc", "def")

        self.assertEqual({}, roster.assignments)

        RosterAssignments.create(self.context, roster.sequence_no, person1.identifier, "role")
        self.assertEqual({person1.identifier: "role"}, roster.assignments)

        RosterAssignments.create(self.context, roster.sequence_no, person2.identifier, "role")
        self.assertEqual({person1.identifier: "role", person2.identifier: "role"}, roster.assignments)

    def test_create_error_invalid_roster(self) -> None:
        """
        Tests that invalid roster numbers are rejected.
        """
        person = Persons.create(self.context, "id", "abc", "def")

        # Empty roster sequence number.
        with self.assertRaises(InvalidArgumentError):
            RosterAssignments.create(self.context, "", person.identifier, "role")

        # Non-numeric value.
        with self.assertRaises(InvalidArgumentError):
            RosterAssignments.create(self.context, "abc", person.identifier, "role")

        # Roster that doesn't exist.
        with self.assertRaises(ObjectNotFoundError):
            RosterAssignments.create(self.context, "123", person.identifier, "role")

    def test_create_error_invalid_person(self) -> None:
        """
        Tests that invalid person identifiers are rejected.
        """
        roster = Rosters.create(self.context, "123")

        # Empty person id.
        with self.assertRaises(ObjectNotFoundError):
            RosterAssignments.create(self.context, roster.sequence_no, "", "role")

        # Person that doesn't exist.
        with self.assertRaises(ObjectNotFoundError):
            RosterAssignments.create(self.context, roster.sequence_no, "xyz", "role")

    def test_create_error_invalid_role(self) -> None:
        """
        Tests that invalid roles are rejected.
        """
        roster = Rosters.create(self.context, "123")
        person = Persons.create(self.context, "id", "abc", "def")

        with self.assertRaises(InvalidArgumentError):
            RosterAssignments.create(self.context, roster.sequence_no, person.identifier, "")

    def test_delete_success(self) -> None:
        """
        Tests that it is possible to remove an assignment.
        """
        roster = Rosters.create(self.context, "123")
        person = Persons.create(self.context, "id", "abc", "def")
        RosterAssignments.create(self.context, roster.sequence_no, person.identifier, "role")

        self.assertEqual({person.identifier: "role"}, roster.assignments)

        RosterAssignments.delete(self.context, roster.sequence_no, person.identifier)
        self.assertEqual({}, roster.assignments)

    def test_delete_error_invalid_roster(self) -> None:
        """
        Tests that invalid roster numbers are rejected.
        """
        person = Persons.create(self.context, "id", "abc", "def")

        # Empty roster sequence number.
        with self.assertRaises(InvalidArgumentError):
            RosterAssignments.delete(self.context, "", person.identifier)

        # Non-numeric value.
        with self.assertRaises(InvalidArgumentError):
            RosterAssignments.delete(self.context, "abc", person.identifier)

        # Roster that doesn't exist.
        with self.assertRaises(ObjectNotFoundError):
            RosterAssignments.delete(self.context, "123", person.identifier)

    def test_delete_error_invalid_person(self) -> None:
        """
        Tests that invalid person identifiers are rejected.
        """
        roster = Rosters.create(self.context, "123")

        # Empty person id.
        with self.assertRaises(ObjectNotFoundError):
            RosterAssignments.delete(self.context, roster.sequence_no, "")

        # Person that doesn't exist.
        with self.assertRaises(ObjectNotFoundError):
            RosterAssignments.delete(self.context, roster.sequence_no, "xyz")
