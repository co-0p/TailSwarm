import click
import subprocess
import os


@click.command()
def init():
    click.echo("Starting Node Initialization Process...")


    # Get directory of this Python file
    this_dir = os.path.dirname(os.path.abspath(__file__))
    # Relative path to bash scripts
    ts_script = os.path.join(this_dir, '../shellscripts/install_tailscale.sh')
    docker_script = os.path.join(this_dir, '../shellscripts/install_docker.sh')
    ts_run = subprocess.run(['bash', ts_script], check=True)
    docker_run = subprocess.run(['bash', docker_script], check=True)

    # TODO - make it all work