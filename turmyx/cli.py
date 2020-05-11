import os
from pathlib import Path

import click

from turmyx.config import TurmyxConfig, CfgConfig, YAMLConfig, pass_config
from turmyx.open import turmyx_open
from turmyx.utils import parse_path
from turmyx.scripts import scripts


@click.group()
@click.option('-f', '--file',
              help='Input a different configuration file, rather than the global one.',
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


cli.add_command(turmyx_open)
cli.add_command(scripts)
