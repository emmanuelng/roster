import dataclasses
from builtins import sorted

import click

from dataset.dataclasses.Person import Person
from dataset.datasets.CsvDataset import CsvDataset


@click.command()
@click.argument("identifier")
@click.argument("first_name")
@click.argument("last_name")
def person_add(identifier, first_name, last_name):
    """
    Create a new person.
    """
    person = Person(identifier, first_name, last_name)
    CsvDataset().add_person(person)


@click.command()
@click.argument("identifier")
def person_remove(identifier):
    """
    Delete a person.
    """
    CsvDataset().remove_person(identifier)


@click.command()
@click.argument("person_identifier")
@click.argument("role")
def person_roles_add(person_identifier, role):
    """
    Add a role to a person.
    """
    dataset = CsvDataset()
    person = dataset.get_person(person_identifier)

    if person is not None and not person.has_role(role):
        dataset.remove_person(person_identifier)
        dataset.add_person(dataclasses.replace(person, roles=person.roles + [role]))


@click.command()
@click.argument("user_identifier")
def person_roles_get(person_identifier):
    """
    Display the list of roles of a person.
    """
    person = CsvDataset().get_person(person_identifier)
    if person is not None:
        click.echo(", ".join(person.roles))
    else:
        click.echo("Error: Person not found.", err=True)


@click.command()
def persons_list():
    """
    Display the list of persons.
    """
    persons = sorted(CsvDataset().get_persons(), key=lambda p: p.full_name)
    for person in persons:
        click.echo(f"{person.full_name} ({person.identifier})")
