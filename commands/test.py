import click
import subprocess

from utils.checks import assert_on_correct_tailnet
from utils.helpers import get_all_node_labels

from utils.helpers import am_devmachine


@click.command()
# @click.option(
#     "--environment",
#     required=True
# )
def test():
    print(am_devmachine())