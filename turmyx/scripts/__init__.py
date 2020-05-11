import os
from pathlib import Path
import click

from turmyx.config import pass_config, TurmyxConfig
from turmyx.commands import CommandEntry


@click.group(name="scripts")
@pass_config
def scripts(config_ctx: TurmyxConfig):
    """
    Manage scripts to be launched when using `turmyx open` commands.
    """


@scripts.command("install")
@click.option('-m', '--merge', is_flag=True, help="If provided a merge will be attempted.")
@pass_config
def install(config_ctx: TurmyxConfig, merge: bool):
    """
     Install the provided file to `turmyx -f` into the system one.

     If you provide a file to turmyx using the syntax `turmyx -f turmyxconf_local.yml`, the `turmyxconf_local.yml`
     configuration will be saved onto the system one.

     If you provide the `--merge` option, a merge will be attempted, expect some overrides.
    """

    config_cls = type(config_ctx)

    default_conf = config_cls().load()
    default_conf_file = default_conf.config_file

    if merge:
        default_conf.load(config_ctx.config_file).save(default_conf_file)
        return
    else:
        config_ctx.save(config_file=default_conf_file)
        return


@scripts.command("add")
@click.option('--editor', is_flag=True, help="Configure new script as file editor.")
@click.option('--opener', is_flag=True, help="Configure new script as url opener.")
@click.option(
    '-n', '--name',
    type=str,
    nargs=1,
    help='A name for the script configuration, otherwise it will be guessed from script path.'
)
@click.option(
    '-d', '--default',
    is_flag=True,
    help='The script will be saved as default one for the given mode, --name option and any argument in '
         'CASES_LIST would be ignored.'
)
@click.argument(
    'script',
    type=str,
    required=True
)
@click.argument(
    'cases_list',
    type=str,
    nargs=-1,
    required=False,
)
@pass_config
def add(
        config_ctx: TurmyxConfig,
        editor: bool,
        opener: bool,
        script: str,
        cases_list: str,
        name: str,
        default: bool
):
    """
    Add a new script configuration.

    Examples:

        turmyx add editor nano txt md ini

        turmyx add --name radare editor r2 exe

        turmyx add opener youtube-dl youtube.com youtu.be

        turmyx add --default opener qr


    Adds a new script to Turmyx, the configuration name is set inline by an OPTION --name, otherwise the name is
    guessed from script name. The argument MODE has to be 'editor' or 'opener' and sets the run environment of the
    script. SCRIPT must be a valid path to the script/program, and must be executable, otherwise when executing it
    would lead to an exception. Finally, the CASES_LIST will contain a list of extensions or domains to be used along
     with the script.

    """

    if not editor ^ opener:
        click.echo("You must choose --editor or --opener, can't be both or neither.")
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

        if editor:
            config_ctx.set_file_editor(command)
        if opener:
            config_ctx.set_url_opener(command)

        config_ctx.save()

    except FileNotFoundError:
        click.echo("Given script not found or not executable.")
        return


@scripts.command("remove")
@click.option('--editor', is_flag=True, help="Remove script only in the file editors list.")
@click.option('--opener', is_flag=True, help="Remove script only in the url openers list.")
@click.argument(
    'script',
    type=str,
    required=True
)
@pass_config
def remove(
        config_ctx: TurmyxConfig,
        editor: bool,
        opener: bool,
        script: str
):
    """
    Removes script configuration.
    """

    # Boolean trick to ensure both are computed when both flags are False:
    if not opener ^ editor:
        editor = opener = True

    if editor and script in config_ctx.get_editors():
        config_ctx.remove_file_editor(script)
        click.echo(f"'{script}' file editor successfully removed!")
    else:
        click.echo(f"'{script}' not found or skipped in file editors.")

    if opener and script in config_ctx.get_openers():
        config_ctx.remove_url_opener(script)
        click.echo(f"'{script}' url opener successfully removed!")
    else:
        click.echo(f"'{script}' not found or skipped in url openers.")

    config_ctx.save()


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


