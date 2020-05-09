import click

from turmyx.config import TurmyxConfig
from turmyx.commands import Command
from turmyx.utils import parse_extension, parse_domain


@click.command()
@click.argument('file',
                type=click.Path(exists=True),
                required=False,
                )
@click.pass_obj
def editor(config_ctx: TurmyxConfig, file: str):
    """
    Run suitable editor for any file in Termux.

    You can soft-link this command with:

    ln -s ~/bin/termux-file-editor $PREFIX/bin/turmyx-file-editor
    """

    command: Command = config_ctx.get_file_editor(parse_extension(file))

    try:
        output, errors = command(file).communicate()
        click.echo(output)
    except FileNotFoundError:
        click.echo("'{}' not found. Please check the any typo or installation.".format(command.command))


@click.command()
@click.argument('url',
                type=str,
                required=False,
                )
@click.pass_obj
def opener(config_ctx: TurmyxConfig, url):
    """
    Run suitable parser for any url in Termux.

    You can soft-link this command with:

    ln -s ~/bin/termux-url-opener $PREFIX/bin/turmyx-url-opener
    """

    command: Command = config_ctx.get_url_opener(parse_domain(url))

    try:
        output, errors = command(url).communicate()
        click.echo(output)
    except FileNotFoundError:
        click.echo("'{}' not found. Please check the any typo or installation.".format(command.command))