import subprocess
from zoneinfo import available_timezones

import click
import yaml

from utils.checks import assert_on_correct_tailnet
from utils.helpers import get_manager_nodes_in_environment, run_remote, simple_run_remote, docker_remote, get_all_node_labels



@click.command()
@click.option(
    "--environment",
    required=True,
    help="Name of the environment"
)
def deploy(environment):
    deploy_successful = True
    assert_on_correct_tailnet()
    with open('tailswarm.yml', 'r') as file:
        config = yaml.safe_load(file)

    environment_spec = config.get("environments", {}).get(environment, {})
    nodes = environment_spec.get("nodes", [])
    stacks = environment_spec.get("stacks", [])

    managers = get_manager_nodes_in_environment(environment)
    manager = managers.pop()
    print(manager)

    click.echo(f"Deploying to environment {environment} via manager {manager}")

    # Copy over data
    # click.echo("Recopying dockerswarm directory on manager nodes..")
    # run_remote("rm -rf ~/dockerswarm", manager)
    # args = ["scp", "-o", "StrictHostKeyChecking=no", "-r", "dockerswarm/", f"root@{manager}:~/dockerswarm"]
    # subprocess.run(
    #     args
    # )

    # Labels
    environment_node_labels = get_all_node_labels(environment)
    # print(environment_node_labels)

    for node in nodes:
        node_name = node.get("name")
        desired_stack_labels = set(node.get("deploy", []))
        existing_stack_labels = environment_node_labels[node_name]

        rm_stack_labels = existing_stack_labels.difference(desired_stack_labels)
        add_stack_labels = desired_stack_labels.difference(existing_stack_labels)

        for rm in rm_stack_labels:
            docker_remote(["docker", "node", "update", "--label-rm", rm, node_name], manager)
        for add in add_stack_labels:
            docker_remote(["docker", "node", "update", "--label-add", f"{add}=true", node_name], manager)

        click.echo(f"To {node_name} added {len(add_stack_labels)} labels, removed {len(rm_stack_labels)}")

    # Stack deploys
    for stack in stacks:
        click.echo(f"Deploying stack {stack}...")
        # cmd = [
        #     "docker", "stack", "deploy", "--prune", \
        #     "--detach=false", "--with-registry-auth", \
        #     "-c", f"dockerswarm/stacks/{stack}.yml", stack
        # ]
        # print(" ".join(cmd))
        # print(docker_run(" ".join(cmd), manager))
        cmd = " ".join([
            "cat", f"dockerswarm/stacks/{stack}.yml", "|", \
            "ssh", f"root@{manager}", "docker", "stack", "deploy", "--prune", \
            "--detach=true", "--with-registry-auth", \
            "-c", "-", stack
        ])
        print(cmd)
        run = subprocess.run(cmd, shell=True)
        if run.returncode != 0:
            click.echo(f"Error This Deploy Did Not Succeed ({stack})")
            deploy_successful = False
    click.echo("Stacks deployed")
    if not deploy_successful:
        click.echo("Not everything went right, check logs.")
    #
    # # TODO take down unneeded stacks