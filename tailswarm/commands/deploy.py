from zoneinfo import available_timezones

import click
import yaml

from utils.checks import assert_on_correct_tailnet
from utils.helpers import get_manager_nodes_in_environment, run_remote, docker_remote, get_all_node_labels


@click.command()
@click.option(
    "--environment",
    required=True,
    help="Name of the environment"
)
def deploy(environment):
    assert_on_correct_tailnet()
    with open('tailswarm.yaml', 'r') as file:
        config = yaml.safe_load(file)

    environment_spec = config.get("environments", {}).get(environment, {})
    nodes = environment_spec.get("nodes", [])
    stacks = environment_spec.get("stacks", [])

    managers = get_manager_nodes_in_environment(environment)
    manager = managers.pop()

    click.echo(f"Deploying to environment {environment} via manager {manager}")

    # Copy over data
    # TODO

    # Stack deploys
    for stack in stacks:
        click.echo(f"Deploying stack {stack}...")
        cmd = ["docker", "stack", "deploy", "--compose-file", f"dockerswarm/stacks/{stack}.yml", stack]
        print(docker_remote(cmd, manager))
    click.echo("Stacks deployed")

    # TODO take down unneeded stacks

    # Labels
    environment_node_labels = get_all_node_labels(environment)
    print(environment_node_labels)

    for node in nodes:
        node_name = node.get("name")
        print(node_name)
        desired_stack_labels = set(node.get("deploy", []))
        existing_stack_labels = environment_node_labels[node_name]

        rm_stack_labels = existing_stack_labels.difference(desired_stack_labels)
        add_stack_labels = desired_stack_labels.difference(existing_stack_labels)
