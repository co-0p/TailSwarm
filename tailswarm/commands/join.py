import click


@click.command()
@click.option(
    "--environment", 
    required=True, 
    help="Name of the environment to join e.g. 'production-environment'"
)
@click.option(
    "--tailscale_token", 
    required=True,
    help="Token to join tailnet"
)
def join(environment, tailscale_token):
    # TODO
    print(environment, tailscale_token)