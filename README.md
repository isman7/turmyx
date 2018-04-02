# turmyx

turmyx is a script launcher for `Termux` app to link `termux-url-opener` and `termux-url-opener` with custom scripts.

## Installation

turmyx is in a really alpha state. If you want to try to test it in your Termux, you can follow this:

```
git clone https://github.com/isman7/turmyx.git
cd turmyx
pip install -e .
cd ~
mkdir bin
ln -s bin/termux-url-opener $PREFIX/bin/turmyx-url-opener
ln -s bin/termux-file-editor $PREFIX/bin/turmyx-file-editor
```

## Commands

At this early point, it accepts only two commands related with the input url/file from the external worl to Termux.

Some help outputs:

```
$ turmyx --help
Usage: turmyx [OPTIONS] COMMAND [ARGS]...

  This is turmyx! A script launcher for external files/url in
  Termux. Enjoy!

Options:
  --help  Show this message and exit.

Commands:
  editor  Run suitable editor for any file in Termux.
  opener  Run suitable parser for any url in Termux.

```

```
$ turmyx editor --help
This is turmyx! A script launcher for external files/url in Termux. Enjoy!
Usage: turmyx editor [OPTIONS] [FILE]

  Run suitable editor for any file in Termux.

  You can soft-link this command with:

  ln -s ~/bin/termux-file-editor $PREFIX/bin/turmyx-file-editor

Options:
  --help  Show this message and exit.
```

## configuration.ini

A simple configparser class is used, you can simple edit it and play. For URL parsing, a demonstration with a QR
encoding is shown (you need to `pip install qrcode` module to be able to use it).

Enjoy!

# TODO LIST

- `--config-file` argument to turmyx main command.
- ~~A url parser to be able to differ domains~~.
- More than one parser/editor per url/file. With CLI input to choose.
- Additional commands such as: `add`, `remove`, etc to configure scripts from terminal, not only config file.
- Possible output handlers, such as: Termux-api.

