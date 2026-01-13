import click


@click.command()
@click.option(
    "--environment", 
    required=False, 
    help="Defaults to current environment (if exists)"
)
def find_manager():
    # TODO
    pass