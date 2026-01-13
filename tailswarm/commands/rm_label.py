import click


@click.command()
@click.option(
    "--node_name", 
    required=True, 
    help="Name of the node to remove label from"
)
@click.option(
    "--label", 
    required=True,
    help="Label name to remove"
)
def rm_label():
    # TODO
    pass