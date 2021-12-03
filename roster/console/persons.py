from builtins import sorted

import click

from dataset.Dataset import Dataset
from dataset.objects.Person import Person


@click.command()
@click.argument("identifier")
@click.argument("first_name")
@click.argument("last_name")
def person_add(identifier, first_name, last_name):
    """
    Create a new person.
    """
    person = Person(identifier, first_name, last_name)
    Dataset().add_person(person)


@click.command()
@click.argument("identifier")
def person_remove(identifier):
    """
    Delete a person.
    """
    Dataset().remove_person(identifier)


@click.command()
@click.argument("user_identifier")
@click.argument("role")
def person_roles_add(person_identifier, role):
    """
    Add a role to a person.
    """
    person = Dataset().get_person(person_identifier)
    if person is not None:
        person.add_role(role)


@click.command()
@click.argument("user_identifier")
def person_roles_get(person_identifier):
    """
    Display the list of roles of a person.
    """
    person = Dataset().get_person(person_identifier)
    if person is not None:
        click.echo(", ".join(person.roles))
    else:
        click.echo("Error: Person not found.", err=True)


@click.command()
def persons_list():
    """
    Display the list of persons.
    """
    persons = sorted(Dataset().get_persons(), key=lambda p: p.full_name)
    for person in persons:
        click.echo(person.full_name + " (" + person.identifier + ")")
