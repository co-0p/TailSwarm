import click


@click.command()
@click.option(
    "--environment", 
    required=False, 
    help="Status to given environment (defaults to current environment)"
)
def status(node_name):
    # TODO
    pass