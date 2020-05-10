import click

from turmyx.config import pass_config


@click.group()
@pass_config
def scripts():
    """
    Manage scripts to be launched when using `turmyx open` commands.
    """


@scripts.command()
@pass_config
def add():
    pass


@scripts.command()
@pass_config
def remove():
    pass


@scripts.command()
@pass_config
def list():
    pass


@scripts.command()
@pass_config
def link():
    pass

