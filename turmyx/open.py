import click

from turmyx.config import TurmyxConfig
from turmyx.commands import Command
from turmyx.utils import parse_path, parse_url


@click.group(
    name="open",  # enforce naming to avoid collision with python open()
    # invoke_without_command=True,
)
@click.pass_obj
def turmyx_open(config_ctx: TurmyxConfig):
    """
    Open a file or URL inside termux the user's preferred application.
    """
    pass


@turmyx_open.command("file")
@click.argument('file',
                type=click.Path(exists=True),
                )
@click.pass_obj
def editor(config_ctx: TurmyxConfig, file: str):
    """
    Run suitable editor for any file in Termux.
    """

    command: Command = config_ctx.get_file_editor(parse_path(file))

    try:
        output, errors = command(file).communicate()
        click.echo(output)
    except FileNotFoundError:
        click.echo("'{}' not found. Please check the any typo or installation.".format(command.command))


@turmyx_open.command("url")
@click.argument('url',
                type=str,
                required=False,
                )
@click.pass_obj
def opener(config_ctx: TurmyxConfig, url):
    """
    Run suitable parser for any url in Termux.
    """

    command: Command = config_ctx.get_url_opener(parse_url(url))

    try:
        output, errors = command(url).communicate()
        click.echo(output)
    except FileNotFoundError:
        click.echo("'{}' not found. Please check the any typo or installation.".format(command.command))