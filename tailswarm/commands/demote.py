import click


@click.command()
@click.option(
    "--node_name", 
    required=True, 
    help="Name of the node to demote from manager"
)
def demote(node_name):
    # TODO
    pass