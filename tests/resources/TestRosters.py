from TestCase import TestCase
from app.errors.InvalidArgumentError import InvalidArgumentError
from app.resources.Patterns import Patterns
from app.resources.PersonAbsences import PersonAbsences
from app.resources.PersonRoles import PersonRoles
from app.resources.Persons import Persons
from app.resources.Rosters import Rosters
from database.errors.DuplicateKeyError import DuplicateKeyError
from database.errors.ObjectNotFoundError import ObjectNotFoundError
from generator.errors.NotEnoughResourcesError import NotEnoughResourcesError


class TestRosters(TestCase):

    def test_create_success(self):
        """
        Tests that it is possible to create a roster.
        """
        # Add a roster.
        roster = Rosters.create(self.context, "123")

        # Check that the fields are correctly initialized.
        self.assertEqual(123, roster.sequence_no)

        # Check that the roster was added to the database.
        self.assertEqual(1, len(Rosters.list(self.context)))
        self.assertEqual(roster, Rosters.list(self.context)[0])

    def test_create_error_invalid_sequence_no(self):
        """
        Tests that invalid sequence numbers are rejected when creating a new roster.
        """
        with self.assertRaises(InvalidArgumentError):
            Rosters.create(self.context, "abc")

        with self.assertRaises(InvalidArgumentError):
            Rosters.create(self.context, "")

    def test_create_error_duplicate_sequence_no(self):
        """
        Tests that it isn't possible to create two rosters with the same sequence number.
        """
        with self.assertRaises(DuplicateKeyError):
            Rosters.create(self.context, "123")
            Rosters.create(self.context, "123")

        self.assertEqual(1, len(Rosters.list(self.context)))

    def test_delete_success(self):
        """
        Tests that it is possible to delete a roster.
        """
        # Create two rosters and check that they were saved.
        roster1 = Rosters.create(self.context, "123")
        roster2 = Rosters.create(self.context, "456")
        self.assertEqual([roster1, roster2], Rosters.list(self.context))

        # Delete one roster.
        Rosters.delete(self.context, "123")
        self.assertEqual([roster2], Rosters.list(self.context))

    def test_delete_success_unknown_sequence_no(self):
        """
        Tests that the delete method accepts unknown sequence numbers.
        """
        Rosters.create(self.context, "123")
        self.assertEqual(1, len(Rosters.list(self.context)))

        Rosters.delete(self.context, "456")
        self.assertEqual(1, len(Rosters.list(self.context)))

    def test_delete_error_invalid_sequence_no(self):
        """
        Tests that invalid sequence numbers are rejected when deleting a roster.
        """
        with self.assertRaises(InvalidArgumentError):
            Rosters.delete(self.context, "abc")

        with self.assertRaises(InvalidArgumentError):
            Rosters.delete(self.context, "")

    def test_generate_success(self):
        """
        Tests a simple roster generation.
        """
        # Generate three persons.
        person1 = Persons.create(self.context, "person1", "Person1", "Person1")
        PersonRoles.add(self.context, person1.identifier, "role1")

        person2 = Persons.create(self.context, "person2", "Person2", "Person2")
        PersonRoles.add(self.context, person2.identifier, "role2")

        person3 = Persons.create(self.context, "person3", "Person3", "Person3")
        PersonRoles.add(self.context, person2.identifier, "role3")

        # Add a pattern.
        pattern = Patterns.create(self.context, "pattern1")
        Patterns.set(self.context, pattern.identifier, "role1", 1)
        Patterns.set(self.context, pattern.identifier, "role2", 1)

        # Generate the roster.
        roster = Rosters.generate(self.context, 123)
        self.assertTrue(roster.is_assigned(person1, "role1"))
        self.assertTrue(roster.is_assigned(person2, "role2"))
        self.assertFalse(roster.is_assigned(person3))

    def test_generate_success_considers_absences(self):
        """
        Tests that absent persons aren't scheduled.
        """
        # Generate two persons.
        person1 = Persons.create(self.context, "person1", "Person1", "Person1")
        PersonRoles.add(self.context, person1.identifier, "role")

        person2 = Persons.create(self.context, "person2", "Person2", "Person2")
        PersonRoles.add(self.context, person2.identifier, "role")

        # Add a pattern.
        pattern = Patterns.create(self.context, "pattern")
        Patterns.set(self.context, pattern.identifier, "role", 1)

        # Add an absence for the first person and generate a roster.
        PersonAbsences.create(self.context, person1.identifier, 123)
        roster = Rosters.generate(self.context, 123)
        self.assertFalse(roster.is_assigned(person1))
        self.assertTrue(roster.is_assigned(person2, "role"))

        # Delete the roster and remove the absence.
        Rosters.delete(self.context, 123)
        PersonAbsences.delete(self.context, person1.identifier, 123)

        # Add an absence for the second person and generate a roster.
        PersonAbsences.create(self.context, person2.identifier, 123)
        roster = Rosters.generate(self.context, 123)
        self.assertTrue(roster.is_assigned(person1, "role"))
        self.assertFalse(roster.is_assigned(person2))

    def test_generate_error_not_enough_resources(self):
        """
        Tests a roster creation when there are not enough resources.
        """
        # Generate a person.
        person1 = Persons.create(self.context, "person1", "Person1", "Person1")
        PersonRoles.add(self.context, person1.identifier, "role")

        # Add a pattern.
        pattern = Patterns.create(self.context, "pattern")
        Patterns.set(self.context, pattern.identifier, "role", 5)

        # Generate the roster, since there is not enough persons, we expect an error.
        with self.assertRaises(NotEnoughResourcesError):
            Rosters.generate(self.context, 123)

    def test_generate_error_invalid_sequence_no(self):
        """
        Tests that invalid sequence numbers are rejected when generating a roster.
        """
        with self.assertRaises(InvalidArgumentError):
            Rosters.generate(self.context, "abc")

        with self.assertRaises(InvalidArgumentError):
            Rosters.generate(self.context, "")

    def test_get_success(self):
        """
        Tests that it is possible to get an existing roster.
        """
        roster_create = Rosters.create(self.context, "123")
        roster_get = Rosters.get(self.context, roster_create.sequence_no)
        self.assertEqual(roster_create, roster_get)

    def test_get_error_unknown_sequence_no(self):
        """
        Tests that an error is raised when the sequence number doesn't exist.
        """
        with self.assertRaises(ObjectNotFoundError):
            Rosters.get(self.context, "123")

    def test_get_error_invalid_sequence_no(self):
        """
        Tests that an error is raised when the sequence number is invalid.
        """
        with self.assertRaises(InvalidArgumentError):
            Rosters.get(self.context, "abc")

        with self.assertRaises(InvalidArgumentError):
            Rosters.get(self.context, "")

    def test_list_success(self):
        """
        Tests that it is possible to get the list of rosters.
        """
        self.assertEqual([], Rosters.list(self.context))

        # Add two rosters. Check that they are sorted by sequence number.
        roster1 = Rosters.create(self.context, "456")
        roster2 = Rosters.create(self.context, "123")
        self.assertEqual([roster2, roster1], Rosters.list(self.context))
