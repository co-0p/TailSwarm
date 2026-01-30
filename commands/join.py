import subprocess

import click
import requests

from utils.checks import assert_on_correct_tailnet
from utils.helpers import get_self_environment, get_manager_nodes_in_environment, get_current_tailnet_suffic

from utils.checks import assert_am_not_devmachine


@click.command()
def join():
    assert_on_correct_tailnet()
    assert_am_not_devmachine()
    current_environment = get_self_environment()
    current_ts_suffix = get_current_tailnet_suffic()
    manager_nodes = get_manager_nodes_in_environment(current_environment)

    if len(manager_nodes) == 0:
        raise click.ClickException("No managers found in this environment")

    manager_node = manager_nodes[0]
    response = requests.get(f"http://{manager_node}.{current_ts_suffix}:8080/join").json()
    print(response)

    token = response["join_token"]

    subprocess.run(["docker", "swarm", "join", "--token", token,  f"{manager_node}:2377"], shell=True)
