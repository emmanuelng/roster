import click

from dataset.dataclasses.Pattern import Pattern
from dataset.datasets.CsvDataset import CsvDataset


@click.command()
@click.argument("identifier")
def pattern_add(identifier):
    """
    Create a new pattern.
    """
    CsvDataset().add_pattern(Pattern(identifier))


@click.command()
@click.argument("identifier")
@click.argument("role")
@click.argument("number")
def pattern_assignments_set(identifier, role, number):
    """
    Set an assignment of a pattern.
    """
    p = CsvDataset().get_pattern(identifier)
    if p is None:
        click.echo("Error: Pattern not found.")
        return

    p.set_assignment(role, int(number))


@click.command()
@click.argument("identifier")
def pattern_get(identifier):
    """
    Display the details of a pattern.
    """
    p = CsvDataset().get_pattern(identifier)
    click.echo(p if p is not None else "Error: Pattern not found")


@click.command()
@click.argument("identifier")
def pattern_remove(identifier):
    """
    Delete a pattern.
    """
    CsvDataset().remove_pattern(identifier)


@click.command()
def patterns_list():
    """
    Display the list of patterns.
    """
    for pattern in CsvDataset().get_patterns():
        click.echo(pattern.identifier)
