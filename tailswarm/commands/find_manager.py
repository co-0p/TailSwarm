import click
from utils import helpers


@click.command()
def find_manager():
    return helpers.get_manager_name()