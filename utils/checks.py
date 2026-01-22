import json

import click
import subprocess
from utils import helpers
from utils.helpers import get_tailswarm_config, get_current_tailnet_suffic


def assert_am_manager():
    if not helpers.am_manager():
        raise click.ClickException("This can only be run from a manager node")


def assert_am_worker():
    if helpers.am_manager():
        raise click.ClickException("This can only be run from a worker node")

def assert_on_correct_tailnet():
    ts_config = get_tailswarm_config()
    defined_ts_suffix = ts_config["tailnet-suffix"].strip()

    if defined_ts_suffix != get_current_tailnet_suffic():
        raise click.ClickException("Tailnet suffix in config file does not match current Tailnet suffix")