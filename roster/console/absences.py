import click

from dataset.datasets.CsvDataset import CsvDataset


@click.command()
@click.argument("identifier")
@click.argument("roster_sequence_no")
def absence_add(identifier, roster_sequence_no):
    """
    Add an absence.
    """
    person = CsvDataset().get_person(identifier)
    CsvDataset().add_absence(int(roster_sequence_no), person)


@click.command()
@click.argument("identifier")
@click.argument("roster_sequence_no")
def absence_remove(identifier, roster_sequence_no):
    """
    Remove an absence.
    """
    person = CsvDataset().get_person(identifier)
    CsvDataset().remove_absence(int(roster_sequence_no), person)


@click.command()
@click.argument("identifier")
def absences_persons_get(identifier):
    """
    Get the absences of a person.
    """
    person = CsvDataset().get_person(identifier)
    for absence in CsvDataset().get_absences(person=person):
        click.echo(absence.roster_sequence_no)


@click.command()
@click.argument("sequence_no")
def absences_rosters_get(sequence_no):
    """
    Get the absences of a roster.
    """
    for absence in CsvDataset().get_absences(roster_sequence_no=int(sequence_no)):
        click.echo(str(absence.person_identifier))
