import click

from dataset.Dataset import Dataset


@click.command()
@click.argument("identifier")
@click.argument("roster_sequence_no")
def absence_add(identifier, roster_sequence_no):
    """
    Add an absence.
    """
    person = Dataset().get_person(identifier)
    Dataset().add_absence(int(roster_sequence_no), person)


@click.command()
@click.argument("identifier")
@click.argument("roster_sequence_no")
def absence_remove(identifier, roster_sequence_no):
    """
    Remove an absence.
    """
    person = Dataset().get_person(identifier)
    Dataset().remove_absence(int(roster_sequence_no), person)


@click.command()
@click.argument("identifier")
def absences_persons_get(identifier):
    """
    Get the absences of a person.
    """
    person = Dataset().get_person(identifier)
    for roster_sequence_no in Dataset().get_person_absences(person):
        click.echo(roster_sequence_no)


@click.command()
@click.argument("sequence_no")
def absences_rosters_get(sequence_no):
    """
    Get the absences of a roster.
    """
    for person in Dataset().get_roster_absences(int(sequence_no)):
        click.echo(str(person))
