import subprocess
import click


@click.command()
@click.option(
    "--node-name", 
    required=True, 
    help="Name of the node to ssh into"
)
@click.option(
    "--user", 
    required=True,
    default="root",
    help="User name to use (default:root)"
)
def ssh(node_name, user):
    subprocess.run(["tailscale", "ssh", f"{user}@{node_name}"])