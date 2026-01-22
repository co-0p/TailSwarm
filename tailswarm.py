
from commands.admin_server import admin_server
from commands.demote import demote
from commands.deploy import deploy
from commands.find_manager import find_manager
from commands.init import init
from commands.test import test
from commands.join import join
from commands.promote import promote
import click


@click.group()
def cli():
    pass


# Add all the commands:
cli.add_command(admin_server)
cli.add_command(demote)
cli.add_command(deploy)
cli.add_command(find_manager)
cli.add_command(init)
cli.add_command(promote)
cli.add_command(join)
cli.add_command(test)


if __name__ == '__main__':
    cli()
