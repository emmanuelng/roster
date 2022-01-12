from TestCase import TestCase
from app.errors.InvalidArgumentError import InvalidArgumentError
from app.resources.Patterns import Patterns
from database.errors.DuplicateKeyError import DuplicateKeyError
from database.errors.ObjectNotFoundError import ObjectNotFoundError


class TestPatterns(TestCase):

    def test_create_success(self):
        """
        Tests that it is possible to create a pattern.
        """
        # Add a pattern.
        pattern = Patterns.create(self.context, "id")

        # Check that the fields are correctly initialized.
        self.assertEqual("id", pattern.identifier)

        # Check that the pattern was added to the database.
        self.assertEqual(1, len(self.database.get_patterns()))
        self.assertEqual(pattern, self.database.get_patterns()[0])

    def test_create_error_duplicate_identifiers(self):
        """
        Tests that it is not possible to create two persons with the same identifiers.
        """
        # Add a pattern to the database.
        pattern = Patterns.create(self.context, "test_id")
        self.assertEqual(1, len(self.database.get_patterns()))

        # Try to add another pattern with the same id. An exception must be raised.
        with self.assertRaises(DuplicateKeyError):
            Patterns.create(self.context, "test_id")

        # Check that only the first pattern is in the database.
        self.assertEqual(1, len(self.database.get_patterns()))
        self.assertEqual(pattern, self.database.get_patterns()[0])

    def test_delete_success(self):
        """
        Tests that it is possible to delete a pattern.
        """
        # Add two patterns.
        pattern1 = Patterns.create(self.context, "id1")
        pattern2 = Patterns.create(self.context, "id2")
        self.assertEqual(2, len(self.database.get_patterns()))

        # Delete one pattern.
        Patterns.delete(self.context, pattern1.identifier)
        self.assertEqual(1, len(self.database.get_patterns()))
        self.assertEqual(pattern2, self.database.get_patterns()[0])

    def test_delete_success_unknown_id(self):
        """
        Tests that it is possible to provide an unknown person_id without any error.
        """
        # Add a pattern.
        Patterns.create(self.context, "test_id")
        self.assertEqual(1, len(self.database.get_patterns()))

        # Invoke the delete method with invalid identifiers.
        Patterns.delete(self.context, "xyz")
        Patterns.delete(self.context, None)

        # Check that no pattern was deleted.
        self.assertEqual(1, len(self.database.get_patterns()))

    def test_get_success(self):
        """
        Tests that the get method is able to find an existing pattern.
        """
        pattern = Patterns.create(self.context, "test_id")
        self.assertEqual(pattern, Patterns.get(self.context, "test_id"))

    def test_get_error_unknown_id(self):
        """
        Tests that the get method raises an exception when an unknown person_id is provided.
        """
        with self.assertRaises(ObjectNotFoundError):
            Patterns.get(self.context, "xyz")

        with self.assertRaises(ObjectNotFoundError):
            Patterns.get(self.context, None)

    def test_list_success(self):
        """
        Tests that it is possible to get the list of patterns.
        """
        self.assertEqual(0, len(Patterns.list(self.context)))

        # Add three patterns.
        pattern1 = Patterns.create(self.context, "b")
        pattern2 = Patterns.create(self.context, "c")
        pattern3 = Patterns.create(self.context, "a")

        # Check that the list contains the three patterns.
        patterns = Patterns.list(self.context)
        self.assertEqual(3, len(patterns))

        # Check that the persons are sorted by id.
        self.assertEqual(pattern3, patterns[0], "The patterns are not sorted by id.")
        self.assertEqual(pattern1, patterns[1], "The patterns are not sorted by id.")
        self.assertEqual(pattern2, patterns[2], "The patterns are not sorted by id.")

    def test_set_success(self):
        """
        Tests that it is possible to set an assignment of a pattern.
        """
        # Add a pattern.
        pattern = Patterns.create(self.context, "id")
        self.assertEqual({}, pattern.assignments)

        # Set an assignment.
        Patterns.set(self.context, "id", "role1", "2")
        pattern = Patterns.get(self.context, "id")
        self.assertEqual({"role1": 2}, pattern.assignments)

        # Set another assignment.
        Patterns.set(self.context, "id", "role2", "1")
        pattern = Patterns.get(self.context, "id")
        self.assertEqual({"role1": 2, "role2": 1}, pattern.assignments)

    def test_set_success_modify_existing_assignment(self):
        """
        Tests that it is possible to set an existing assignment.
        """
        # Add a pattern.
        Patterns.create(self.context, "id")

        # Set an assignment.
        Patterns.set(self.context, "id", "role", "2")
        pattern = Patterns.get(self.context, "id")
        self.assertEqual({"role": 2}, pattern.assignments)

        # Modify the assignment.
        Patterns.set(self.context, "id", "role", "8")
        pattern = Patterns.get(self.context, "id")
        self.assertEqual({"role": 8}, pattern.assignments)

    def test_set_error_unknown_pattern(self):
        """
        Tests that an exception is raised when one tries to set an assignment of an unknown pattern.
        """
        with self.assertRaises(ObjectNotFoundError):
            Patterns.set(self.context, "xyz", "role", "2")

    def test_set_error_invalid_role(self):
        """
        Tests that an error is raised when the role is invalid.
        """
        Patterns.create(self.context, "id")

        with self.assertRaises(InvalidArgumentError):
            Patterns.set(self.context, "id", "", "1")

    def test_set_error_invalid_number(self):
        """
        Tests that errors are raised when the number value is invalid.
        """
        Patterns.create(self.context, "id")

        # Non-numeric value.
        with self.assertRaises(InvalidArgumentError):
            Patterns.set(self.context, "id", "role", "abc")

        # Empty value.
        with self.assertRaises(InvalidArgumentError):
            Patterns.set(self.context, "id", "role", "")

        # Zero.
        with self.assertRaises(InvalidArgumentError):
            Patterns.set(self.context, "id", "role", "0")

        # Negative value.
        with self.assertRaises(InvalidArgumentError):
            Patterns.set(self.context, "id", "role", "-1")

        # Check that no assignment was saved.
        pattern = Patterns.get(self.context, "id")
        self.assertEqual({}, pattern.assignments)
