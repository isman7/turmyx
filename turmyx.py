import os
import click
import subprocess
from configparser import ConfigParser, ExtendedInterpolation


DIR_PATH = os.path.dirname(os.path.realpath(__file__))

CONFIG = ConfigParser(interpolation=ExtendedInterpolation())
CONFIG.read(os.path.join(DIR_PATH, "configuration.ini"))


def guess_file_command(extension, configuration):
    assert isinstance(extension, str)
    assert isinstance(configuration, ConfigParser)

    for section in configuration.sections():
        if extension in configuration[section]["extensions"]:
            return configuration[section]["command"]


@click.group(invoke_without_command=True)
def cli():
    """Example script."""
    click.echo('This is turmyx! A script launcher for external files/url in Termux. Enjoy!')


@cli.command()
@click.argument('file',
                type=click.Path(exists=True),
                required=False,
                )
def editor(file):
    if isinstance(file, str):
        file_name = os.path.basename(file)
        extension = file_name.split('.')[-1]
        command = guess_file_command(extension, CONFIG)

        if command:
            try:
                subprocess.check_call([command, file])
            except FileNotFoundError:
                click.echo("'{}' not found. Please check the any typo or installation.".format(command))
        else:
            click.echo("¯\_ツ_/¯ : Extension not recognised.")


@cli.command()
@click.argument('url',
                type=str,
                required=False,
                )
def opener(url):
    if isinstance(url, str):
        for section in CONFIG.sections():
            if "opener" in section:
                command = CONFIG[section]["command"]
                try:
                    subprocess.check_call([command, url])
                except FileNotFoundError:
                    click.echo("'{}' not found. Please check the any typo or installation.".format(command))

