import os
import click
import subprocess
from configparser import ConfigParser, ExtendedInterpolation
from urllib.parse import urlparse


class TurmyxConfig(ConfigParser):
    DIR_PATH = os.path.dirname(os.path.realpath(__file__))

    def __init__(self):
        self.config_path = os.path.join(self.DIR_PATH, "configuration.ini")
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
def cli(config_ctx):
    """
    This is turmyx! A script launcher for external files/url in Termux. Enjoy!
    """
    config_ctx.read(config_ctx.config_path)
    # click.echo(click.get_current_context().get_help())


@cli.command()
@click.option('--merge',
              'mode',
              flag_value='merge',
              help="Merge new file config into the existing file.")
@click.option('--symlink',
              'mode',
              flag_value='symlink',
              help="Symlink to the provided configuration file.")
@click.argument('file',
                type=click.Path(exists=True),
                required=False,
                )
@turmyx_config_context
def config(config_ctx, file, mode):
    """
    Set configuration file by overriding the last one.

    You can use a mode flag to configure how to save the new configuration. Both can't be combined, so the last one
    to be called will be the used by the config command.
    """

    abs_path = os.path.abspath(file)
    click.echo("Absolute path for provided file: {}".format(abs_path))

    new_config = TurmyxConfig()
    new_config.read(abs_path)

    if not mode:
        with open(config_ctx.config_path, "w") as config_f:
            new_config.write(config_f)
        click.echo("Succesfully saved.")
    elif mode == "merge":
        click.echo("Not implemented yet.")
    elif mode == "symlink":
        click.echo("Not implemented yet.")


@cli.command()
@click.argument('file',
                type=click.Path(exists=True),
                required=False,
                )
@turmyx_config_context
def editor(config_ctx, file):
    """
    Run suitable editor for any file in Termux.

    You can soft-link this command with:

    ln -s ~/bin/termux-file-editor $PREFIX/bin/turmyx-file-editor
    """
    if isinstance(file, str):
        section = config_ctx.guess_file_command(file)
        command = config_ctx[section]["command"]

        try:
            if "command_args" in section:
                arguments = config_ctx[section]["command_args"]
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
def opener(config_ctx, url):
    """
    Run suitable parser for any url in Termux.

    You can soft-link this command with:

    ln -s ~/bin/termux-url-opener $PREFIX/bin/turmyx-url-opener
    """
    if isinstance(url, str):
        section = config_ctx.guess_url_command(url)
        command = config_ctx[section]["command"]

        try:
            if "command_args" in section:
                arguments = config_ctx[section]["command_args"]
                call_args = [command] + arguments.split(" ") + [url]
            else:
                call_args = [command, url]

            click.echo(" ".join(call_args))
            subprocess.check_call(call_args)

        except FileNotFoundError:
            click.echo("'{}' not found. Please check the any typo or installation.".format(command))

