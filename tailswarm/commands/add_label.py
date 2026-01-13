import click


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
def add_label(node_name, label):
    # TODO
    print(node_name, label)