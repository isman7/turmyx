import os
import click
import subprocess
from configparser import ConfigParser, ExtendedInterpolation
from urllib.parse import urlparse


DIR_PATH = os.path.dirname(os.path.realpath(__file__))

CONFIG = ConfigParser(interpolation=ExtendedInterpolation())
CONFIG.read(os.path.join(DIR_PATH, "configuration.ini"))


def guess_file_command(file, configuration):
    assert isinstance(file, str)
    assert isinstance(configuration, ConfigParser)

    file_name = os.path.basename(file)
    extension = file_name.split('.')[-1]

    for section in configuration.sections():
        if "default" not in section and "editor" in section:
            if extension in configuration[section]["extensions"]:
                return section

    return "editor:default"


@click.group(invoke_without_command=True)
def cli():
    """
    This is turmyx! A script launcher for external files/url in Termux. Enjoy!
    """
    click.echo('This is turmyx! A script launcher for external files/url in Termux. Enjoy!')


@cli.command()
@click.argument('file',
                type=click.Path(exists=True),
                required=False,
                )
def editor(file):
    """
    Run suitable editor for any file in Termux.

    You can soft-link this command with:

    ln -s ~/bin/termux-file-editor $PREFIX/bin/turmyx-file-editor
    """
    if isinstance(file, str):
        section = guess_file_command(file, CONFIG)
        command = CONFIG[section]["command"]

        try:
            if "command_args" in section:
                arguments = CONFIG[section]["command_args"]
                call_args = [command] + arguments.split(" ") + [file]
            else:
                call_args = [command, file]

            subprocess.check_call([command, file])

            # print(CONFIG["editor:default"])
            # click.echo("¯\_ツ_/¯ : Extension not recognised.")

            print(call_args)
            subprocess.check_call(call_args)

        except FileNotFoundError:
            click.echo("'{}' not found. Please check the any typo or installation.".format(command))


@cli.command()
@click.argument('url',
                type=str,
                required=False,
                )
def opener(url):
    """
    Run suitable parser for any url in Termux.

    You can soft-link this command with:

    ln -s ~/bin/termux-url-opener $PREFIX/bin/turmyx-url-opener
    """
    if isinstance(url, str):
        for section in CONFIG.sections():
            if "opener" in section and "default" in section:
                command = CONFIG[section]["command"]
                try:
                    subprocess.check_call([command, url])
                except FileNotFoundError:
                    click.echo("'{}' not found. Please check the any typo or installation.".format(command))

