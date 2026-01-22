import click
import subprocess

from utils.checks import assert_am_manager
from utils.helpers import get_self_name


@click.command()
@click.option(
    "--node-name",
    required=False, 
    help="Name of the node to demote from manager"
)
def demote(node_name):
    assert_am_manager()
    subprocess.run(["docker", "node", "demote", get_self_name()], shell=True)