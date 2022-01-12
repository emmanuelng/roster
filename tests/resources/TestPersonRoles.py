from TestCase import TestCase
from app.errors.InvalidArgumentError import InvalidArgumentError
from app.resources.PersonRoles import PersonRoles
from app.resources.Persons import Persons
from database.errors.ObjectNotFoundError import ObjectNotFoundError


class TestPersonRoles(TestCase):

    def test_add_success(self):
        """
        Tests that it is possible to add a role to a person.
        """
        # Add a person.
        person = Persons.create(self.context, "id", "f_name", "l_name")
        self.assertEqual([], person.roles)

        # Add a role.
        PersonRoles.add(self.context, "id", "role1")
        self.assertEqual(["role1"], PersonRoles.get(self.context, "id"))

        # Add another role.
        PersonRoles.add(self.context, "id", "role2")
        self.assertEqual(["role1", "role2"], PersonRoles.get(self.context, "id"))

    def test_add_success_existing_role(self):
        """
        Tests that it is possible to add a role that a person already has.
        """
        # Add a person with a role.
        Persons.create(self.context, "id", "f_name", "l_name")
        PersonRoles.add(self.context, "id", "role")

        # Add the same role.
        PersonRoles.add(self.context, "id", "role")
        self.assertEqual(["role"], PersonRoles.get(self.context, "id"))

    def test_add_error_invalid_role(self):
        """
        Tests that it is not possible to add an empty role.
        """
        Persons.create(self.context, "id", "f_name", "l_name")
        with self.assertRaises(InvalidArgumentError):
            PersonRoles.add(self.context, "id", "")

    def test_get_success(self):
        """
        Tests that it is possible to get the roles of a person.
        """
        # Add a person.
        Persons.create(self.context, "id", "f_name", "l_name")
        roles = PersonRoles.get(self.context, "id")
        self.assertEqual([], roles)

        # Add roles.
        PersonRoles.add(self.context, "id", "roleB")
        PersonRoles.add(self.context, "id", "roleC")
        PersonRoles.add(self.context, "id", "roleA")

        # Get the roles. Check that they are sorted in alphabetical order.
        roles = PersonRoles.get(self.context, "id")
        self.assertEqual(["roleA", "roleB", "roleC"], roles)

        # Check that the list of role is similar to the one obtained through GetPerson.
        person = Persons.get(self.context, "id")
        self.assertCountEqual(person.roles, roles)

    def test_get_error_unknown_person(self):
        """
        Tests that an exception is raised if the person id is invalid.
        """
        with self.assertRaises(ObjectNotFoundError):
            PersonRoles.get(self.context, "xyz")

    def test_remove_success(self):
        """
        Tests that it is possible to remove a role.
        """
        # Add a person.
        Persons.create(self.context, "id", "f_name", "l_name")

        # Add two roles.
        PersonRoles.add(self.context, "id", "role1")
        PersonRoles.add(self.context, "id", "role2")
        self.assertEqual(["role1", "role2"], PersonRoles.get(self.context, "id"))

        # Remove one role.
        PersonRoles.remove(self.context, "id", "role1")
        self.assertEqual(["role2"], PersonRoles.get(self.context, "id"))

    def test_remove_error_unknown_person(self):
        """
        Tests that an exception is raised if the person id is invalid.
        """
        with self.assertRaises(ObjectNotFoundError):
            PersonRoles.remove(self.context, "xyz", "role")

    def test_remove_success_unknown_role(self):
        """
        Tests that it is possible to remove a role that a person doesn't have.
        """
        Persons.create(self.context, "id", "f_name", "l_name")
        PersonRoles.add(self.context, "id", "role")
        self.assertEqual(["role"], PersonRoles.get(self.context, "id"))

        PersonRoles.remove(self.context, "id", "xyz")
        self.assertEqual(["role"], PersonRoles.get(self.context, "id"))

    def test_remove_error_invalid_role(self):
        """
        Tests that an exception is raised when the role argument is empty.
        """
        Persons.create(self.context, "id", "f_name", "l_name")
        with self.assertRaises(InvalidArgumentError):
            PersonRoles.remove(self.context, "id", "")
