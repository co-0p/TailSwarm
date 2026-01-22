import click
import subprocess
import time

from utils.helpers import get_self_environment, get_manager_nodes_in_environment


@click.command()
def init():
    click.echo("Starting Node Initialization Process...")

    # TAILSCALE
    click.echo("Installing Tailscale...")
    subprocess.run("curl -fsSL https://tailscale.com/install.sh | sh", shell=True)
    tailscale_authkey = input("Enter your Tailscale auth key with correct environment tag: ")
    subprocess.run(f"""
        tailscale up \
        --authkey={tailscale_authkey} \
        --ssh \
        --accept-routes
        """,
       shell=True
    )
    time.sleep(5)
    subprocess.run("tailscale set --ssh", shell=True) # The first time doesnt always seem to work
    click.echo("Tailscale Installation Complete!")

    # DOCKER
    click.echo("Installing Docker...")
    subprocess.run("curl -sSL https://get.docker.com/ | sh", shell=True)
    subprocess.run("adduser dockeruser", shell=True)
    subprocess.run("usermod -aG docker dockeruser", shell=True)
    subprocess.run("systemctl restart docker", shell=True)
    click.echo("Docker Installation Complete!")

    # JOIN or BOOTSTRAP
    click.echo("Looking for an existing Docker Swarm...")
    current_environment = get_self_environment()
    existing_manager_nodes = get_manager_nodes_in_environment(current_environment)
    if len(existing_manager_nodes) == 0:
        click.echo(f"Found no existing manager nodes in environment {current_environment}")
        click.echo("Bootstrapping new cluster...")

