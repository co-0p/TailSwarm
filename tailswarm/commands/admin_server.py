import click
from lib.bottle import route, run
from utils import checks


@click.command()
def admin_server():
    checks.assert_am_manager()
    run(host='localhost', port=7777)
