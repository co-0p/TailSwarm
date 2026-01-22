import click
import subprocess

from utils.checks import assert_on_correct_tailnet
from utils.helpers import get_all_node_labels


@click.command()
# @click.option(
#     "--environment",
#     required=False
# )
def test():
    output = subprocess.run(
        ["docker", "swarm", "join-token", "worker"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout

    key = output.strip().split(" ")[-2]