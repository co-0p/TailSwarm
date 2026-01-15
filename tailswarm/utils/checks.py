import click
from utils import helpers

def assert_am_manager():
    if not helpers.am_manager():
        raise click.ClickException("This can only be run from a manager node")


def assert_am_worker():
    if helpers.am_manager():
        raise click.ClickException("This can only be run from a worker node")