from TestCase import TestCase
from app.resources.Persons import Persons
from dataset.errors.DuplicateKeyError import DuplicateKeyError
from dataset.errors.ObjectNotFoundError import ObjectNotFoundError


class TestPersons(TestCase):
    """
    Persons resource tests.
    """

    def test_create_success(self):
        """
        Tests that it is possible to create a new person.
        """
        # Add a person.
        person = Persons.create(self.context, "test_id", "test_f_name", "test_l_name")

        # Check that the person was added to the dataset.
        self.assertEqual(1, len(self.dataset.get_persons()))
        self.assertEqual(person, self.dataset.get_persons()[0])

    def test_create_error_duplicate_identifiers(self):
        """
        Tests that it is not possible to create two persons with the same identifiers.
        """
        # Add a person to the dataset.
        person = Persons.create(self.context, "test_id", "person_1", "person_1")
        self.assertEqual(1, len(self.dataset.get_persons()))

        # Try to add another person with the same id. An exception must be raised.
        with self.assertRaises(DuplicateKeyError):
            Persons.create(self.context, "test_id", "person_2", "person_2")

        # Check that only the first person is in the dataset.
        self.assertEqual(1, len(self.dataset.get_persons()))
        self.assertEqual(person, self.dataset.get_persons()[0])

    def test_delete_success(self):
        """
        Tests that it is possible to delete a person.
        """
        # Add two person.
        person1 = Persons.create(self.context, "id1", "test_f_name", "test_l_name")
        person2 = Persons.create(self.context, "id2", "test_f_name", "test_l_name")
        self.assertEqual(2, len(self.dataset.get_persons()))

        # Delete the person.
        Persons.delete(self.context, person1.identifier)
        self.assertEqual(1, len(self.dataset.get_persons()))
        self.assertEqual(person2, self.dataset.get_persons()[0])

    def test_delete_success_unknown_id(self):
        """
        Tests that it is possible to provide an unknown identifier without any error.
        """
        # Add a person
        Persons.create(self.context, "test_id", "person_1", "person_1")
        self.assertEqual(1, len(self.dataset.get_persons()))

        # Invoke the delete method with invalid identifiers.
        Persons.delete(self.context, "xyz")
        Persons.delete(self.context, None)

        # Check that no person was deleted.
        self.assertEqual(1, len(self.dataset.get_persons()))

    def test_get_success(self):
        """
        Tests that the get method is able to find an existing person.
        """
        person = Persons.create(self.context, "test_id", "test_f_name", "test_l_name")
        self.assertEqual(person, Persons.get(self.context, "test_id"))

    def test_get_error_unknown_id(self):
        """
        Tests that the get method raises an exception when an unknown identifier is provided.
        """
        with self.assertRaises(ObjectNotFoundError):
            Persons.get(self.context, "xyz")

        with self.assertRaises(ObjectNotFoundError):
            Persons.get(self.context, None)

    def test_list_success(self):
        """
        Tests that it is possible to get the list of persons.
        """
        self.assertEqual(0, len(Persons.list(self.context)))

        # Add two persons.
        person1 = Persons.create(self.context, "id1", "person1", "person1")
        person2 = Persons.create(self.context, "id2", "person2", "person2")

        # Check that the list contains the two persons (order is not guaranteed).
        self.assertEqual(2, len(Persons.list(self.context)))
        self.assertIn(person1, Persons.list(self.context))
        self.assertIn(person2, Persons.list(self.context))
