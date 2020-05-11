import os
from pathlib import Path

import click

from turmyx.commands import CommandEntry
from turmyx.config import TurmyxConfig, CfgConfig, YAMLConfig, pass_config
from turmyx.open import turmyx_open
from turmyx.utils import parse_path
from turmyx.scripts import scripts


@click.group()
@click.option('-f', '--file',
              help='Input a different configuration file, rather than global one.',
              required=False,)
@click.pass_context
def cli(ctx: click.Context, file):
    """
    This is turmyx! A script launcher for external files/url in Termux. Enjoy!
    """

    if file:
        config_file = file
        config_file = Path(config_file)
        assert config_file.exists()

        config_extension = parse_path(config_file)

        if config_extension in ("ini", "cfg"):
            config = CfgConfig()
        elif config_extension in ("yml", "yaml"):
            config = YAMLConfig()

        ctx.obj = config.load(config_file)
        click.echo(f"Successfully loaded configuration from: {config_file}")

    else:
        print(YAMLConfig().config_file)
        ctx.obj = YAMLConfig().load()


@cli.command()
@click.option('--merge',
              'mode',
              flag_value='merge',
              help="Merge new file config into the existing file.")
@click.option('--symlink',
              'mode',
              flag_value='symlink',
              help="Symlink to the provided configuration file.")
@click.option('--view',
              is_flag=True,
              help="Output the actual configuration of Turmyx scripts.")
@click.argument('file',
                type=click.Path(exists=True),
                required=False,
                )
@pass_config
def config(config_ctx: TurmyxConfig, file, mode, view):
    """
    Set configuration file.

    You can use a mode flag to configure how to save the new configuration. Both can't be combined, so the last one
    to be called will be the used by the config command.
    """

    if file:

        os.remove(CONFIG_FILE)

        abs_path = os.path.abspath(file)
        click.echo("Absolute path for provided file: {}".format(abs_path))

        new_config = CfgConfig()
        new_config.read(abs_path)

        # TODO: validate this config file.

        if not mode:
            new_config.save()
            click.echo("Succesfully saved into {}.".format(CONFIG_FILE))
        elif mode == "merge":
            # First attempt, only overriding partials:

            config_ctx.load(abs_path)
            config_ctx.save()
            click.echo("Succesfully merged: {} \n into: {} \n and saved.".format(abs_path, CONFIG_FILE))

        elif mode == "symlink":
            os.symlink(abs_path, CONFIG_FILE)
            click.echo("Succesfully linked: {} \n to: {}.".format(CONFIG_FILE, abs_path))

    if view:
        click.echo(config_ctx.config_file.read_text())


# cli.add_command(editor)
# cli.add_command(opener)
cli.add_command(turmyx_open)
cli.add_command(scripts)
