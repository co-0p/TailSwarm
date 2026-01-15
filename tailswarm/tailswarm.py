#!/usr/bin/env python3
import click

# Import each command function here and add them in tailswarm.py
from commands.add_label import add_label
from commands.admin_server import admin_server
from commands.demote import demote
from commands.deploy_stacks import deploy_stacks
from commands.find_manager import find_manager
from commands.init import init
from commands.promote import promote
from commands.rm_label import rm_label


@click.group()
def cli():
    pass


# Add all the commands:
cli.add_command(add_label)
cli.add_command(admin_server)
cli.add_command(demote)
cli.add_command(deploy_stacks)
cli.add_command(find_manager)
cli.add_command(init)
cli.add_command(promote)
cli.add_command(rm_label)


if __name__ == '__main__':
    cli()
