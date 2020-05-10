import os
from pathlib import Path
import click

from turmyx.config import pass_config, TurmyxConfig


@click.group(name="scripts")
@pass_config
def scripts(config_ctx: TurmyxConfig):
    """
    Manage scripts to be launched when using `turmyx open` commands.
    """


@scripts.command("add")
@pass_config
def add(config_ctx: TurmyxConfig):
    pass


@scripts.command("remove")
@pass_config
def remove(config_ctx: TurmyxConfig):
    pass


@scripts.command("list")
@click.option('--editors', is_flag=True, help="Only show file editor scripts.")
@click.option('--openers', is_flag=True, help="Only show url opener scripts.")
@pass_config
def scripts_list(config_ctx: TurmyxConfig, editors: bool, openers: bool):
    """
    List all available scripts to edit a file or open an url.
    """

    # Boolean trick to ensure both are computed when both flags are False:
    if not openers ^ editors:
        editors = openers = True

    if editors:
        click.echo(f"{config_ctx.get_editors()}")

    if openers:
        click.echo(f"{config_ctx.get_openers()}")


@scripts.command("link")
@click.option('--editors', is_flag=True, help="Only link termux-file-editor script.")
@click.option('--openers', is_flag=True, help="Only link termux-url-opener script.")
@click.option('-y', '--yes', is_flag=True, help="Avoid confirm if override is necessary")
def link(editors: bool, openers: bool, yes: bool):
    """
    Link `turmyx open file` and `turmyx open url` to termux scripts.

    The links will be as follow, using the short-cut scripts:

         $PREFIX/bin/turmyx-open → ~/bin/termux-file-editor
         $PREFIX/bin/turmyx-open-url → ~/bin/termux-url-opener

    """

    # Boolean trick to ensure both are computed when both flags are False:
    if not openers ^ editors:
        editors = openers = True

    prefix = Path(os.environ.get("PREFIX"))
    home = Path(os.environ.get("HOME"))

    assert prefix.exists() and home.exists()

    turmyx_open = prefix / "bin" / "turmyx-open"
    turmyx_open_url = prefix / "bin" / "turmyx-open-url"

    termux_file_editor = home / "bin" / "termux-file-editor"
    termux_url_opener = home / "bin" / "termux-url-opener"

    if editors:
        if termux_file_editor.exists():
            if yes or click.confirm(f"Are you sure you want to override {termux_file_editor}?"):
                os.remove(termux_file_editor)
                os.symlink(turmyx_open, termux_file_editor)
        else:
            if not termux_file_editor.parent.exists():
                os.makedirs(termux_file_editor.parent)
            os.symlink(turmyx_open, termux_file_editor)

    if openers:
        if termux_url_opener.exists():
            if yes or click.confirm(f"Are you sure you want to override {termux_url_opener}?"):
                os.remove(termux_url_opener)
                os.symlink(turmyx_open_url, termux_url_opener)
        else:
            if not termux_url_opener.parent.exists():
                os.makedirs(termux_url_opener.parent)
            os.symlink(turmyx_open_url, termux_url_opener)


