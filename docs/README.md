# Nexis CLI

Nexis is a powerful command-line (CLI) tool for
interacting with the Nexis (or your) API.

## Installation

You can install the CLI from the [Python Package Index](https://pypi.org/project/nexis/).
Simply install it with your preferred package manager:

```sh
pip install nexis
poetry add nexis
pipx install nexis
```

## Getting Started

After installing Nexis, you can run it from your terminal:

```sh
nexis [command] [options] [arguments]
```

To see a list of available commands, run:

```sh
nexis --help
```

## Usage

Running `Nexis` without any arguments will show you the help message.

```text
Usage:
  command [options] [arguments]

Options:
  -h, --help            Display help for the given command.
  -q, --quiet           Do not output any message.
  -V, --version         Display this application version.
      --ansi            Force ANSI output.
      --no-ansi         Disable ANSI output.
  -n, --no-interaction  Do not ask any interactive question.
  -D, --dev             Use development options defined in nexis.toml.
  -C, --config=CONFIG   Use the specified configuration file.
  -v|vv|vvv, --verbose  Increase the verbosity of messages:
                          1 for normal output
                          2 for more verbose output
                          3 for debug.

Available commands:
  help  Display help for a command.
  list  List commands.
  ...
```

## Commands

Nexis comes with a variety of commands.
For detailed information on each command, refer to the
[Commands Documentation](./commands/README.md)

## Configuration

Nexis can be configured using the `nexis.toml` TOML file.
The configuration file load order is as follows:

1. `~/.config/nexis/nexis.toml`
2. `$CWD/nexis.toml`
3. Path from `-C/--config` option (if provided)

For detailed information on the configuration file,
refer to the [Configuration Documentation](./config.md)

## Closing

If you encounter any problems or have questions, please
feel free to [open an issue](https://github.com/caffeine-addictt/nexis/issues/new).
If you enjoy using Nexis, please consider [sponsoring us](https://github.com/sponsors/caffeine-addictt)
or giving us a [✨ star](https://github.com/caffeine-addictt/nexis/stargazers)!
