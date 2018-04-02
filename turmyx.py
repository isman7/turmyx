import os
import click
import subprocess
from configparser import ConfigParser, ExtendedInterpolation
from urllib.parse import urlparse


DIR_PATH = os.path.dirname(os.path.realpath(__file__))


class TurmyxConfig(ConfigParser):
    def __init__(self):
        super(TurmyxConfig, self).__init__(interpolation=ExtendedInterpolation())

    def guess_file_command(self, file):
        assert isinstance(file, str)
        assert isinstance(self, ConfigParser)

        file_name = os.path.basename(file)
        extension = file_name.split('.')[-1]

        for section in self.sections():
            if "default" not in section and "editor" in section:
                if extension in self[section]["extensions"]:
                    return section

        return "editor:default"

    def guess_url_command(self, url):
        assert isinstance(url, str)
        assert isinstance(self, ConfigParser)

        url_parsed = urlparse(url)
        domain = url_parsed.netloc

        if not domain:
            print("Failed to parse URL. Attempt default opener.")
            return "opener:default"

        for section in self.sections():
            if "default" not in section and "opener" in section:
                print(section)
                if domain in self[section]["domains"]:
                    return section

        return "opener:default"


turmyx_config_context = click.make_pass_decorator(TurmyxConfig, ensure=True)


@click.group(invoke_without_command=True)
@turmyx_config_context
def cli(config):
    """
    This is turmyx! A script launcher for external files/url in Termux. Enjoy!
    """
    config.read(os.path.join(DIR_PATH, "configuration.ini"))
    click.echo('This is turmyx! A script launcher for external files/url in Termux. Enjoy!')


@cli.command()
@click.argument('file',
                type=click.Path(exists=True),
                required=False,
                )
@turmyx_config_context
def editor(config, file):
    """
    Run suitable editor for any file in Termux.

    You can soft-link this command with:

    ln -s ~/bin/termux-file-editor $PREFIX/bin/turmyx-file-editor
    """
    if isinstance(file, str):
        section = config.guess_file_command(file)
        command = config[section]["command"]

        try:
            if "command_args" in section:
                arguments = config[section]["command_args"]
                call_args = [command] + arguments.split(" ") + [file]
            else:
                call_args = [command, file]

            click.echo(" ".join(call_args))
            subprocess.check_call(call_args)

        except FileNotFoundError:
            click.echo("'{}' not found. Please check the any typo or installation.".format(command))


@cli.command()
@click.argument('url',
                type=str,
                required=False,
                )
@turmyx_config_context
def opener(config, url):
    """
    Run suitable parser for any url in Termux.

    You can soft-link this command with:

    ln -s ~/bin/termux-url-opener $PREFIX/bin/turmyx-url-opener
    """
    if isinstance(url, str):
        section = config.guess_url_command(url)
        command = config[section]["command"]

        try:
            if "command_args" in section:
                arguments = config[section]["command_args"]
                call_args = [command] + arguments.split(" ") + [url]
            else:
                call_args = [command, url]

            click.echo(" ".join(call_args))
            subprocess.check_call(call_args)

        except FileNotFoundError:
            click.echo("'{}' not found. Please check the any typo or installation.".format(command))

