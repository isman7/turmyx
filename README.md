# turmyx

`turmyx` is a script launcher for [Termux](https://wiki.termux.com/wiki/Main_Page) app to link `termux-url-opener` and `termux-file-editor` with custom scripts 
and cli programs. 

## Installation

turmyx is in a early state. If you want to try use it in your Termux, you can follow this minimal installation:

```
pip install git+https://github.com/isman7/turmyx.git
```

After that, you must link Termux launcher scripts to `turmyx` entry points: 

```
cd ~
mkdir bin
ln -s $PREFIX/bin/turmyx-url-opener bin/termux-url-opener 
ln -s $PREFIX/bin/turmyx-file-editor bin/termux-file-editor 
```


## Commands

Checking `--help` option from termux, you can find: 

```
$ turmyx --help
Usage: turmyx [OPTIONS] COMMAND [ARGS]...

  This is turmyx! A script launcher for external files/url in Termux. Enjoy!

Options:
  --help  Show this message and exit.

Commands:
  add     Add a new script configuration.
  config  Set configuration file.
  editor  Run suitable editor for any file in Termux.
  opener  Run suitable parser for any url in Termux.
  remove  Removes script configuration.

```

turmyx brings easily the possibility to link certain scripts to certain extensions or domains to be used as a entry 
point for Termux files or urls, then simply:

```      
# Add 'nano' as editor for txt, md and ini files
turmyx add editor nano txt md ini

# Add radare2 as editor for exe files and gave the configuration a name
turmyx add --name radare editor r2 exe

# Add youtube-dl as url opener for youtube domains 
turmyx add opener youtube-dl youtube.com youtu.be

# Add qr as url oponer for any other domain
turmyx add --default opener qr
``` 

You can check also:

```
$ turmyx add --help
Usage: turmyx add [OPTIONS] MODE SCRIPT [CASES_LIST]...

  Add a new script configuration.

  Examples:

      turmyx add editor nano txt md ini

      turmyx add --name radare editor r2 exe

      turmyx add opener youtube-dl youtube.com youtu.be

      turmyx add --default opener qr

  Adds a new script to Turmyx, the configuration is setted inline by an
  OPTION --name, otherwhise the name is guessed from script name. The
  argument MODE has to be 'editor' or 'opener' and sets the run environment
  of the script. SCRIPT must be a valid path to the script/program, and must
  be executable, otherwise when executing it would lead to an exception.
  Finally, the CASES_LIST will contain a list of extensions or domains to be
  used along with the script.

Options:
  --name TEXT  A name for the script configuration, otherwise it will be
               guessed from script path.
  --default    The script will be saved as default one for the given mode,
               --name option and any argument in CASES_LIST would be ignored.
  --help       Show this message and exit.
```

## configuration.ini

The configurations are saved using .ini file scheme, and saved locally into a `configuration.ini` file. You can check
 your accumulate configuration with `turmyx config --view` command: 
 
```
$ turmyx config --view
[editor:default]
command = xdg-open
command_args = --chooser --view

[editor:nano]
command = /bin/nano
extensions = txt md conf

[editor:vim]
command = vim
extensions = py java

[opener:default]
command = qr

[opener:youtube]
command = youtube-dl
domains = youtube.com   youtu.be
```

You can also prepare you configuration.ini in you PC and load them onto turmyx, only check: 

```
$ turmyx config --help
Usage: turmyx config [OPTIONS] [FILE]

  Set configuration file.

  You can use a mode flag to configure how to save the new configuration.
  Both can't be combined, so the last one to be called will be the used by
  the config command.

Options:
  --merge    Merge new file config into the existing file.
  --symlink  Symlink to the provided configuration file.
  --view     Output the actual configuration of Turmyx scripts.
  --help     Show this message and exit.
```


**Enjoy!**

# TODO LIST

- ~~config argument to turmyx main command.~~ config command!
- ~~A url parser to be able to differ domains.~~ urlib.parse!
- ~~Additional commands such as: `add`, `remove`, etc to configure scripts from terminal, not only config file.~~
- ~~Create docker environment~~
- ~~Change INI to YAML~~, well both are supported now. 
- Re-structure CLI commands:
    - ~~Unify `turmyx opener` and `turmyx editor` into `turmyx open`, with `turmyx-open` linked.~~
    - ~~Maintain `turmyx-file-editor`, however map to: `turmyx open file`.~~ → New `turmyx-open`.
    - ~~Maintain `turmyx-url-opener`, however map to: `turmyx open url`.~~ → New `turmyx-open-url`.
    - ~~New `turmyx open install`, to create the symbolic links towards `termux-url-opener` and `termux-file-editor`.~~ 
    - Unify `turmyx add`, `turmyx remove` and `turmyx config --view` into `turmyx scripts`
    - Create a `turmyx -f FILE_PATH --commit` flag that enables saving values from a given config file to the system
     one. Also port here the soft-link feature. 
- Add tests
- Add logger
- More than one parser/editor per url/file. With CLI input to choose.
- Parse Termux-api ?
- Pipelines ? 

     
