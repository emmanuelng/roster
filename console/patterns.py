import click

from dataset.Dataset import Dataset
from dataset.Pattern import Pattern


@click.command()
@click.argument("identifier")
def pattern_add(identifier):
    """
    Create a new pattern.
    """
    Dataset().add_pattern(Pattern(identifier))


@click.command()
@click.argument("identifier")
@click.argument("role")
@click.argument("number")
def pattern_assignment_set(identifier, role, number):
    """
    Set an assignment of a pattern.
    """
    p = Dataset().get_pattern(identifier)
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
    p = Dataset().get_pattern(identifier)
    click.echo(p if p is not None else "Error: Pattern not found")


@click.command()
@click.argument("identifier")
def pattern_remove(identifier):
    """
    Delete a pattern.
    """
    Dataset().remove_pattern(identifier)


@click.command()
def patterns_list():
    """
    Display the list of patterns.
    """
    for pattern in Dataset().get_patterns():
        click.echo(pattern.identifier)
