import click
import subprocess

from utils import helpers


@click.command()
@click.option(
    "--node_name", 
    required=False, 
    help="Name of the node to demote from manager"
)
def demote(node_name):
    subprocess.run(["docker", "node", "demote", helpers.get_self_name()])