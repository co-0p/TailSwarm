import subprocess
import click


@click.command()
@click.argument("name", required=True)
@click.argument('secret', type=click.File('r'), default='-')
def set_secret(name, secret):
    """Read input from pipe or stdin"""
    content = secret.read()
    click.echo(f"Received input: {content}")
    subprocess.run(
        ["docker", "secret", "create", name, "-"],
        input=content.encode('utf-8'),
        text=True
    )