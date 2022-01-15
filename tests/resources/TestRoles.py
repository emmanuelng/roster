from TestCase import TestCase
from app.resources.Patterns import Patterns
from app.resources.PersonRoles import PersonRoles
from app.resources.Persons import Persons
from app.resources.Roles import Roles


class TestRoles(TestCase):

    def test_get_success(self):
        """
        Tests that it is possible to get the list of roles.
        """
        self.assertEqual([], Roles.get(self.context))

        # Add a person with a role.
        Persons.create(self.context, "person", "f_name", "l_name")
        PersonRoles.add(self.context, "person", "roleB")
        self.assertEqual(["roleB"], Roles.get(self.context))

        # Add a pattern with two roles.
        Patterns.create(self.context, "pattern")
        Patterns.set(self.context, "pattern", "roleA", "1")
        Patterns.set(self.context, "pattern", "roleB", "1")
        self.assertEqual(["roleA", "roleB"], Roles.get(self.context))

