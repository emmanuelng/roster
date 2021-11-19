from console.patterns import *
from console.persons import *
from console.rosters import *


@click.group()
def roster_cli():
    """
    Roster generator
    """
    pass


roster_cli.add_command(person_add)
roster_cli.add_command(person_remove)
roster_cli.add_command(person_roles_add)
roster_cli.add_command(person_roles_get)
roster_cli.add_command(persons_list)

roster_cli.add_command(roster_add)
roster_cli.add_command(roster_assign)
roster_cli.add_command(roster_generate)
roster_cli.add_command(roster_get)
roster_cli.add_command(roster_remove)
roster_cli.add_command(roster_person_remove)
roster_cli.add_command(rosters_list)

roster_cli.add_command(pattern_get)
roster_cli.add_command(patterns_list)
roster_cli.add_command(pattern_remove)
roster_cli.add_command(pattern_assignment_set)
