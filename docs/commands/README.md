# Commands

This section describes the commands that `Nexis` supports.

## Global flags and options

Global flags and options can be used in any command.
Simply pass them to the command.

```sh
# For a shorthand flag
nexis -h

# For a longhand flag
nexis --help

# For a shorthand option
nexis -C nexis.toml

# For a longhand option
nexis --config nexis.toml
```

The difference between a flag and an option is that a flag takes no argument,
while an option takes an argument.

### Flags

- `-h, --help` - Show help for the command.
- `-q, --quiet` - Do not output anything.
- `-V, --version` - Show the installed version of the `Nexis.
- `--ansi` - Force ANSI output.
- `-n, --no-interaction` - Do not ask any interactive question.
- `-D, --dev` - When enabled, the command will be executed with development configuration.
- `-v, -vv, -vvv, --verbose` - Set the verbosity of the command.
  1 `v` for normal output,
  2 `v`'s for more verbose output and
  3 `v`'s for debug.

### Options

- `-C, --config <file_path>` - Path to the configuration file to be loaded.

## List of commands

Click on the command names to view detailed documentation for each command.

- [docs](./docs.md)
- [list](./list.md)
