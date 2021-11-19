import click

from configuration.Configuration import Configuration
from dataset.Dataset import Dataset
from dataset.Roster import Roster
from generator.Generator import Generator


@click.command()
@click.argument("sequence_number")
def roster_add(sequence_number):
    """
    Create a new roster.
    """
    Dataset().add_roster(Roster(sequence_number))


@click.command()
@click.argument("sequence_number")
@click.argument("person_identifier")
@click.argument("role")
def roster_assign(sequence_number, person_identifier, role):
    """
    Assign a person to a role.
    """
    roster = Dataset().get_roster(int(sequence_number))
    if roster is None:
        click.echo("Error: Roster not found")
        return

    person = Dataset().get_person(person_identifier)
    if person is None:
        click.echo("Error: Person not found")
        return

    roster.assign(person, role)


@click.command()
@click.option("-s", "--save", is_flag=True, default=False, help="Indicates if the roster must be saved or not.")
@click.argument("sequence_number")
def roster_generate(sequence_number, save):
    """
    Generate a roster.
    """
    generator = Generator(Dataset(), Configuration())
    generated_roster = generator.generate_roster(int(sequence_number))

    if generated_roster is None:
        click.echo("Error: No feasible roster was found.")
        return

    click.echo(str(generated_roster))
    if save:
        Dataset().add_roster(generated_roster)
        click.echo("\nRoster saved!")


@click.command()
@click.argument("sequence_number")
def roster_get(sequence_number):
    """
    Display the details of a specific roster.
    """
    r = Dataset().get_roster(int(sequence_number))
    click.echo(r if r is not None else "Error: Roster not found")


@click.command()
@click.argument("sequence_number")
@click.argument("person_identifier")
def roster_person_remove(sequence_number, person_identifier):
    """
    Remove a person from a roster.
    """
    roster = Dataset().get_roster(int(sequence_number))
    if roster is None:
        click.echo("Error: Roster not found")
        return

    roster.remove_person(person_identifier)


@click.command()
@click.argument("sequence_number")
def roster_remove(sequence_number):
    """
    Remove a roster.
    """
    Dataset().remove_roster(int(sequence_number))


@click.command()
def rosters_list():
    """
    Display the list of all rosters.
    """
    for roster in Dataset().get_rosters():
        click.echo(roster.sequence_no)
