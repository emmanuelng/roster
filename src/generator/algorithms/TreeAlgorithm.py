from __future__ import annotations

from typing import Optional

from database.dataclasses.Pattern import Pattern
from database.dataclasses.Person import Person
from database.dataclasses.Roster import Roster
from generator import Generator
from generator.Algorithm import Algorithm
from generator.errors.InvalidParameterError import InvalidParameterError
from generator.errors.NotEnoughResourcesError import NotEnoughResourcesError


class TreeAlgorithm(Algorithm):
    """
    Tree algorithm. This algorithm uses an assignment tree to determine the best sequence of assignments.
    """

    __quality: str

    def __init__(self, generator: Generator, quality: str) -> None:
        """
        Constructor.

        :param generator: Generator associated to this algorithm.
        :param quality: Quality of the solution. Can either be "high", "medium" or "low". In high quality, all sequences
         of assignments are explored, which is very slow in general. However, the obtained solution is optimal. In
         medium, only the best branches are explored. If at a given step multiple branches seem to have the same
         optimality, all of them are explored. The obtained solution is optimal. In low quality, only the best sequences
         are explored. If multiple branches seem to have the same optimality, only one is chosen arbitrarily and
         explored. The solution might not be optimal, but it is relatively fast.
        """
        super().__init__(generator)
        self.__quality = quality

        if quality != "high" and quality != "medium" and quality != "low":
            raise InvalidParameterError()

    def generate_roster(self, roster_sequence_no: int) -> Roster:
        persons = self.database.get_available_persons(roster_sequence_no)
        rosters = []

        for pattern in self.database.get_patterns():
            try:
                root = _AssignmentNode.get_root_node(roster_sequence_no, pattern, persons)

                node_queue = [root]
                while len(node_queue) > 0:
                    node = node_queue.pop(0)

                    if node.is_leaf:
                        rosters.append(node.build_roster())
                        continue

                    node_queue += self.__select_best_nodes(node.children)
            except NotEnoughResourcesError:
                continue

        if len(rosters) == 0:
            raise NotEnoughResourcesError()

        return max(rosters, key=self.roster_score)

    def __select_best_nodes(self, nodes: list[_AssignmentNode]) -> list[_AssignmentNode]:
        """
        Selects the most optimal nodes from a list of nodes.

        :param nodes: List of nodes.
        :return: List of best nodes. All nodes in the list are equally optimal.
        """
        if self.__quality == "high":
            return nodes

        max_score, best_nodes = None, []

        for node in nodes:
            score = self.__evaluate_node(node)
            if max_score is None or score > max_score:
                max_score, best_nodes = score, []
            if score == max_score:
                best_nodes.append(node)

        if self.__quality == "low":
            return [best_nodes[0]] if len(best_nodes) > 0 else []

        return best_nodes

    def __evaluate_node(self, node: _AssignmentNode) -> float:
        """
        Computes a score indicating the optimality of a node. This function is used to compare nodes by optimality.

        :param node: The node.
        :return: A score between 0 and 1. 1 is best, 0 is worst.
        """
        return self.assignment_score(node.roster_sequence_no, node.person, node.role)


class _AssignmentNode:
    """
    Represents a node in the assignment tree.
    """

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
            roles += [role] * pattern.assignments[role]

        root = _AssignmentNode()

        root.__pattern = pattern
        root.__roster_sequence_no = roster_sequence_no
        root.__remaining_persons = persons
        root.__remaining_roles = roles

        return root

    __roster_sequence_no: int
    __pattern: Optional[Pattern]
    __parent: Optional[_AssignmentNode]
    __person: Optional[Person]
    __role: Optional[str]
    __remaining_persons: list[Person]
    __remaining_roles: list[str]
    __children: Optional[list[_AssignmentNode]]

    def __init__(self):
        """
        Constructor.
        """
        self.__roster_sequence_no = 0
        self.__pattern = None
        self.__parent = None
        self.__person = None
        self.__role = None
        self.__remaining_persons = None
        self.__remaining_roles = None
        self.__children = None

    @property
    def children(self) -> list[_AssignmentNode]:
        """
        Child nodes.
        """
        if self.__children is not None:
            return self.__children

        child_nodes = []

        for role in self.__remaining_roles:
            persons_with_role = list(filter(lambda p: p.has_role(role), self.__remaining_persons))
            if len(persons_with_role) == 0:
                raise NotEnoughResourcesError()

            for person in persons_with_role:
                child_nodes.append(self.__init_child(person, role))

        self.__children = child_nodes
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
        return self.__person

    @property
    def role(self) -> Optional[str]:
        """
        Role.
        """
        return self.__role

    @property
    def roster_sequence_no(self) -> int:
        """
        Sequence number of the roster.
        """
        return self.__roster_sequence_no

    def build_roster(self):
        """
        Builds a roster from this node.

        :return: A roster.
        """
        roster = Roster(self.__roster_sequence_no)
        for role in self.__pattern.roles:
            for person in self.__get_assigned_persons(role):
                roster.assign(person, role)

        return roster

    def __get_assigned_persons(self, role: str = None) -> list[Person]:
        """
        Returns the list of persons assigned so far by this node and its ancestors.

        :param role: If given, only returns the persons assigned to this role.
        :return: List of persons.
        """
        persons = []
        current_node = self

        while current_node is not None:
            current_person, current_role = current_node.__person, current_node.__role
            current_node = current_node.__parent

            if role is not None and role != current_role:
                continue

            persons += [current_person]

        return persons

    def __init_child(self, person: Person, role: str) -> _AssignmentNode:
        """
        Initializes a child node.

        :param person: Person.
        :param role: Role.
        :return: The child node.
        """
        child = _AssignmentNode()

        child.__roster_sequence_no = self.__roster_sequence_no
        child.__pattern = self.__pattern
        child.__parent = self
        child.__person = person
        child.__role = role
        child.__remaining_persons = self.__remaining_persons.copy()
        child.__remaining_roles = self.__remaining_roles.copy()

        child.__remaining_persons.remove(person)
        child.__remaining_roles.remove(role)

        return child
