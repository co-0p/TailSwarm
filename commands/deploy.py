import os
import subprocess
import sys

import click
import yaml

from utils.checks import assert_on_correct_tailnet
from utils.helpers import get_manager_nodes_in_environment, run_remote, simple_run_remote, docker_remote, get_all_node_labels

@click.command()
@click.argument('stacks_to_deploy', nargs=-1, required=True)
@click.option(
    "--environment",
    required=True,
    help="Name of the environment"
)
def deploy(environment, stacks_to_deploy):
    deploy_successful = True
    assert_on_correct_tailnet()
    with open('tailswarm.yml', 'r') as file:
        config = yaml.safe_load(file)

    docker_stacks_dir = config.get("docker-swarm-stacks-directory")
    environment_spec = config.get("environments", {}).get(environment, {})
    nodes = environment_spec.get("nodes", [])
    stacks = environment_spec.get("stacks", [])
    deployment_variables = environment_spec.get("deployment-variables", {})

    if not set(stacks_to_deploy).issubset(set(stacks)):
        click.echo("Error: Not all the given stacks are listed in config file")
        exit(1)

    managers = get_manager_nodes_in_environment(environment)
    manager = managers.pop()

    click.echo(f"Deploying {len(stacks_to_deploy)} stack(s) to environment '{environment}' via manager node '{manager}'")

    # Labels
    environment_node_labels = get_all_node_labels(environment)

    click.echo("")
    click.echo("Updating node labels...")
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

        click.echo(f"  - To node '{node_name}' added {len(add_stack_labels)} labels, removed {len(rm_stack_labels)}")
    click.echo("")

    # Stack deploys
    for stack in stacks:

        if stack not in stacks_to_deploy:
            continue

        click.echo(f"Deploying stack '{stack}'. Injecting {len(deployment_variables)} deployment variables.")
        stack_path = os.path.join(docker_stacks_dir, f"{stack.strip()}.yml")


        args = [
            "docker", "stack", "deploy", "--prune", \
            "--detach=false", "--with-registry-auth", \
            "-c", stack_path, stack
        ]
        # print(" ".join(args))
        try:
            subprocess.run(
                args,
                check=True,
                stdout=sys.stdout, #subprocess.PIPE,
                stderr=subprocess.PIPE,
                env={**os.environ, **deployment_variables, "DOCKER_HOST": f"ssh://root@{manager}" }
            )
        except subprocess.CalledProcessError as e:
            deploy_successful = False
            print("Error occurred:", e.stderr.decode())
            click.echo(f"Error This Deploy Did Not Succeed ({stack})")

        click.echo("")

    click.echo("Deploy step DONE")
    if not deploy_successful:
        click.echo("NOTE: Not everything went right, check logs.")

    # TODO take down unneeded stacks