from __future__ import annotations

from typing import Optional

from dataset.Pattern import Pattern
from dataset.Person import Person
from dataset.Roster import Roster
from generator import Generator
from generator.Algorithm import Algorithm
from generator.errors.InvalidParameterError import InvalidParameterError
from generator.errors.NotEnoughResourcesError import NotEnoughResourcesError


class TreeAlgorithm(Algorithm):

    def __init__(self, generator: Generator, quality: str) -> None:
        """
        Constructor.

        :param generator: Generator associated to this algorithm.
        """
        super().__init__(generator)
        self._quality = quality

        if quality != "high" and quality != "medium" and quality != "low":
            raise InvalidParameterError()

    def generate_roster(self, roster_sequence_no: int) -> Roster:
        persons = self.dataset.get_persons()
        rosters = []

        for pattern in self.dataset.get_patterns():
            try:
                root = _AssignmentNode.get_root_node(roster_sequence_no, pattern, persons)

                node_queue = [root]
                while len(node_queue) > 0:
                    node = node_queue.pop(0)

                    if node.is_leaf:
                        rosters.append(node.build_roster())
                        continue

                    node_queue += self._select_best_nodes(node.children)
            except NotEnoughResourcesError:
                continue

        if len(rosters) == 0:
            raise NotEnoughResourcesError()

        return max(rosters, key=self.roster_score)

    def _select_best_nodes(self, nodes: list[_AssignmentNode]) -> list[_AssignmentNode]:
        """
        Selects the most optimal nodes from a list of nodes.

        :param nodes: List of nodes.
        :return: List of best nodes. All nodes in the list are equally optimal.
        """
        if self._quality == "high":
            return nodes

        max_score, best_nodes = None, []

        for node in nodes:
            score = self._evaluate_node(node)
            if max_score is None or score > max_score:
                max_score, best_nodes = score, []
            if score == max_score:
                best_nodes.append(node)

        if self._quality == "low":
            return [best_nodes[0]] if len(best_nodes) > 0 else []

        return best_nodes

    def _evaluate_node(self, node: _AssignmentNode) -> float:
        """
        Computes a score indicating the optimality of a node. This function is used to compare nodes by optimality.

        :param node: The node.
        :return: A score between 0 and 1. 1 is best, 0 is worst.
        """
        return self.assignment_score(node.roster_sequence_no, node.person, node.role)


class _AssignmentNode:

    @staticmethod
    def get_root_node(roster_sequence_no: int, pattern: Pattern, persons: list[Person]):
        """
        Returns the root node of the assignment tree corresponding to the list of persons and the given pattern.

        :param roster_sequence_no: Sequence number of the roster.
        :param pattern: Pattern.
        :param persons: List of persons.
        :return: The root node.
        """
        roles = []
        for role in pattern.roles:
            roles += [role] * pattern.get_number(role)

        root = _AssignmentNode()

        root._pattern = pattern
        root._roster_sequence_no = roster_sequence_no
        root._remaining_persons = persons
        root._remaining_roles = roles

        return root

    def __init__(self):
        """
        Constructor.
        """
        self._roster_sequence_no = 0
        self._pattern = None
        self._parent = None
        self._person = None
        self._role = None
        self._remaining_persons = None
        self._remaining_roles = None
        self._children = None

    @property
    def children(self) -> list[_AssignmentNode]:
        """
        Child nodes.
        """
        if self._children is not None:
            return self._children

        child_nodes = []

        for role in self._remaining_roles:
            persons_with_role = list(filter(lambda p: p.has_role(role), self._remaining_persons))
            if len(persons_with_role) == 0:
                raise NotEnoughResourcesError()

            for person in persons_with_role:
                child_nodes.append(self._init_child(person, role))

        self._children = child_nodes
        return child_nodes

    @property
    def is_leaf(self) -> bool:
        """
        Indicates if this node is a leaf of the tree or not.
        """
        return len(self.children) == 0

    @property
    def person(self) -> Optional[Person]:
        """
        Person.
        """
        return self._person

    @property
    def role(self) -> Optional[str]:
        """
        Role.
        """
        return self._role

    @property
    def roster_sequence_no(self) -> int:
        """
        Sequence number of the roster.
        """
        return self._roster_sequence_no

    def build_roster(self):
        """
        Builds a roster from this node.

        :return: A roster.
        """
        roster = Roster(self._roster_sequence_no)
        for role in self._pattern.roles:
            for person in self._get_assigned_persons(role):
                roster.assign(person, role)

        return roster

    def _get_assigned_persons(self, role: str = None) -> list[Person]:
        """
        Returns the list of persons assigned so far by this node and its ancestors.

        :param role: If given, only returns the persons assigned to this role.
        :return: List of persons.
        """
        persons = []
        current_node = self

        while current_node is not None:
            current_person, current_role = current_node._person, current_node._role
            current_node = current_node._parent

            if role is not None and role != current_role:
                continue

            persons += [current_person]

        return persons

    def _init_child(self, person: Person, role: str) -> _AssignmentNode:
        """
        Initializes a child node.

        :param person: Person.
        :param role: Role.
        :return: The child node.
        """
        child = _AssignmentNode()

        child._roster_sequence_no = self._roster_sequence_no
        child._pattern = self._pattern
        child._parent = self
        child._person = person
        child._role = role
        child._remaining_persons = self._remaining_persons.copy()
        child._remaining_roles = self._remaining_roles.copy()

        child._remaining_persons.remove(person)
        child._remaining_roles.remove(role)

        return child
