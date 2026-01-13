#!/usr/bin/env python3
import click

# Import each command function here and add them in tailswarm.py
from commands.add_label import add_label
from commands.admin import admin
from commands.demote import demote
from commands.deploy_stacks import deploy_stacks
from commands.find_manager import find_manager
from commands.init import init
from commands.join_web import join_web
from commands.join import join
from commands.name import name
from commands.promote import promote
from commands.rm_label import rm_label
from commands.set_secret import set_secret
from commands.ssh import ssh
from commands.status import status


@click.group()
def cli():
    pass


# Add all the commands:
cli.add_command(add_label)
cli.add_command(admin)
cli.add_command(demote)
cli.add_command(deploy_stacks)
cli.add_command(find_manager)
cli.add_command(init)
cli.add_command(join_web)
cli.add_command(join)
cli.add_command(name)
cli.add_command(promote)
cli.add_command(rm_label)
cli.add_command(set_secret)
cli.add_command(ssh)
cli.add_command(status)


if __name__ == '__main__':
    cli()
