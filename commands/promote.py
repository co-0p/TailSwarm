import click
import subprocess

from utils import checks


@click.command()
@click.option(
    "--node-name",
    required=True, 
    help="Name of the node to promote to manager"
)
def promote(node_name):
    checks.assert_am_manager()
    subprocess.run(["docker", "node", "promote", node_name], shell=True)