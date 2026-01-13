import click


@click.command()
@click.option(
    "--node_name", 
    required=True, 
    help="Name of the node to promote to manager"
)
def promote(node_name):
    # TODO
    pass