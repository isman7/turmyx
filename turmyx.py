import os
import click
import subprocess

TEXT_EDITOR_EXT = [
    'txt',
]

IMG_EDITOR_EXT = [
    'png',
    'jpg',
    'bmp',
]


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
        if extension in TEXT_EDITOR_EXT:
            subprocess.check_call(['nano', file])
            print("(^o^)丿 : Successfully edited with Termux.")
        elif extension in IMG_EDITOR_EXT:
            print("¯\_ツ_/¯ : Not implemented yet, soon!")
        else:
            print("¯\_ツ_/¯ : Extension not recognised.")


@cli.command()
@click.argument('url',
                type=str,
                required=False,
                )
def opener(url):
    if isinstance(url, str):
        pass