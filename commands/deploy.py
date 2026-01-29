import os
import subprocess
import sys
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

    docker_stacks_dir = config.get("docker-swarm-stacks-directory")
    environment_spec = config.get("environments", {}).get(environment, {})
    nodes = environment_spec.get("nodes", [])
    stacks = environment_spec.get("stacks", [])

    managers = get_manager_nodes_in_environment(environment)
    manager = managers.pop()
    print(manager)

    click.echo(f"Deploying to environment {environment} via manager {manager}")

    # Labels
    environment_node_labels = get_all_node_labels(environment)

    for node in nodes:
        node_name = node.get("name")
        desired_stack_labels = set(node.get("deploy-labels", []))
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
        stack_path = os.path.join(docker_stacks_dir, f"{stack.strip()}.yml")
        # cmd = " ".join([
        #     "cat", stack_path, "|", \
        #     "ssh", f"root@{manager}", "docker", "stack", "deploy", "--prune", \
        #     "--detach=true", "--with-registry-auth", \
        #     "-c", "-", stack
        # ])
        # print(cmd)
        # run = subprocess.run(cmd, shell=True)


        args = [
            "docker", "stack", "deploy", "--prune", \
            "--detach=false", "--with-registry-auth", \
            "-c", stack_path, stack
        ]
        # run = subprocess.run(
        #     args,
        #     capture_output=True, text=True, check=True,
        #     env={**os.environ, "DOCKER_HOST": f"ssh://root@{node}" }
        # )
        print(" ".join(args))
        try:
            run = subprocess.run(
                args,  # Replace with your command and arguments
                check=True,                        # Raise CalledProcessError on non-zero exit
                stdout=sys.stdout, #subprocess.PIPE,            # Capture stdout
                stderr=subprocess.PIPE,             # Capture stderr
                env={**os.environ, "DOCKER_HOST": f"ssh://root@{manager}" }
            )
        except subprocess.CalledProcessError as e:
            deploy_successful = False
            print("Error occurred:", e.stderr.decode())
            click.echo(f"Error This Deploy Did Not Succeed ({stack})")

        click.echo("")

    click.echo("Stacks deployed")
    if not deploy_successful:
        click.echo("Not everything went right, check logs.")
    #
    # # TODO take down unneeded stacks