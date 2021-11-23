import click

from configuration.Configuration import Configuration


@click.command()
def config_get_all():
    """
    Get the values of the configuration variables.
    """
    for key, value in Configuration().values.items():
        click.echo(key + ": " + str(value))


@click.command()
@click.argument("key")
def config_get(key):
    """
    Get the value of a configuration variable.
    """
    click.echo(str(Configuration().get(key)))


@click.command()
@click.argument("key")
@click.argument("value")
def config_set(key, value):
    """
    Set the value of a configuration variable.
    """
    Configuration().set(key, value)
