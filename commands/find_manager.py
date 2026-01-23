import click

from utils.helpers import get_manager_nodes_in_environment


@click.command()
@click.option(
    "--environment",
    required=True,
    help="Name of the environment"
)
def find_manager(environment):
    managers = get_manager_nodes_in_environment(environment)
    if len(managers):
        click.echo(managers.pop())