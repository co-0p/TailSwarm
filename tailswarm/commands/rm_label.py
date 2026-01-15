import click
import subprocess


@click.command()
@click.option(
    "--node-name", 
    required=True, 
    help="Name of the node to add label to"
)
@click.option(
    "--label", 
    required=True,
    help="Label name to add"
)
def rm_label(node_name, label):
    subprocess.run([
        "docker",
        "node",
        "update",
        "--label-rm",
        f"{label}=true",
        node_name
    ])