import os
from pathlib import Path

import click

from turmyx.commands import CommandEntry
from turmyx.config import TurmyxConfig, CfgConfig, YAMLConfig, pass_config
from turmyx.utils import parse_path

from turmyx.open import turmyx_open


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


@cli.command()
@click.argument('mode',
                type=str,
                nargs=1,
                )
@click.option('--name',
              type=str,
              nargs=1,
              help='A name for the script configuration, otherwise it will be guessed from script path.'
              )
@click.option('--default',
              is_flag=True,
              help='The script will be saved as default one for the given mode, --name option and any argument in '
                   'CASES_LIST would be ignored.'
              )
@click.argument('script',
                type=str,
                required=True)
@click.argument('cases_list',
                type=str,
                nargs=-1,
                required=False,
                )
@pass_config
def add(config_ctx: TurmyxConfig, script, mode, cases_list, name, default):
    """
    Add a new script configuration.

    Examples:

        turmyx add editor nano txt md ini

        turmyx add --name radare editor r2 exe

        turmyx add opener youtube-dl youtube.com youtu.be

        turmyx add --default opener qr


    Adds a new script to Turmyx, the configuration is setted inline by an OPTION --name, otherwhise the name is
    guessed from script name. The argument MODE has to be 'editor' or 'opener' and sets the run environment of the
    script. SCRIPT must be a valid path to the script/program, and must be executable, otherwise when executing it
    would lead to an exception. Finally, the CASES_LIST will contain a list of extensions or domains to be used along with the script.

    """

    if mode not in ("opener", "editor"):
        click.echo("{} is not 'opener' or 'editor' mode.".format(mode))
        return

    click.echo("Evaluating script: {}".format(script))

    try:
        basename = Path(script).name

        command = CommandEntry(
            command=script,
            name=name if name else basename if not default else "default",
            classes=cases_list,
        )
        click.echo("Absolute path found for script: {}".format(command.command))

        if mode == "editor":
            config_ctx.set_file_editor(command)
        elif mode == "opener":
            config_ctx.set_url_opener(command)

        config_ctx.save()

    except FileNotFoundError:
        click.echo("Given script not found or not executable.")
        return


@cli.command()
@click.argument('mode',
                type=str,
                nargs=1,
                )
@click.argument('script',
                type=str,
                required=True)
@pass_config
def remove(config_ctx: TurmyxConfig, mode, script):
    """
    Removes script configuration.
    """

    if mode not in ("opener", "editor"):
        click.echo("{} is not 'opener' or 'editor' mode.".format(mode))
        return

    try:
        if mode == "editor":
            config_ctx.remove_file_editor(script)
        elif mode == "opener":
            config_ctx.remove_url_opener(script)

        config_ctx.save()

        click.echo("Script configuration successfully removed!")

    except ValueError:
        click.echo("Configuration not found.")
        # section_guesses = []
        # for section in config_ctx.sections():
        #     if script in section:
        #         section_guesses.append(section)
        #
        # if section_guesses:
        #     click.echo("Maybe you want to say:\n{}".format(
        #         "\n".join(section_guesses)
        #     ))

