from __future__ import annotations
from importlib import import_module
from typing import Callable

from cleo.commands.command import Command
from cleo.exceptions import CleoLogicError
from cleo.loaders.factory_command_loader import FactoryCommandLoader


"""
A list of strings that represent the commands that should be executed.

Each string should only contain a single command like how it would be
executed in the terminal. Command grouping should be separated with spaces.

The file name in nexis/console/commands/ will be the name of the command dot py.
Subgroups will grouped with directories. And the file shall contain a class
using the command name plus "command" in title case.

Duplicate commands will throw an error.

Example 1:
  nexis/console/commands_loader.py
    COMMANDS = ["login"]

  nexis/console/commands/login.py
    from nexis.console.commands import BaseCommand
    class LoginCommand(BaseCommand):
      # Command implementation here

  type 'nexis login' in the terminal

Example 2:
  nexis/console/commands_loader.py
    COMMANDS = ["auth login"]

  nexis/console/commands/auth/login.py
    from nexis.console.commands import BaseCommand
    class LoginCommand(BaseCommand):
      # Command implementation here

  type 'nexis auth login' in the terminal
"""
COMMANDS: list[str] = [
    "docs",
]


def load_command(name: str) -> Callable[[], Command]:
    """
    Returns a function that loads the command

    Parameters
    ----------
    :param name: The name of the command (Subgroups denoted with spaces)

    Returns
    -------
    :return: A function that loads the command
    """

    def _load() -> Command:
        paths = name.split(" ")
        module = import_module("nexis.console.commands." + ".".join(paths))
        command_class = getattr(module, "".join(a.title() for a in paths) + "Command")

        return command_class()

    return _load


class CommandLoader(FactoryCommandLoader):
    def register_factory(self, name: str, factory: Callable[[], Command]) -> None:
        if name in self._factories:
            raise CleoLogicError(f'The command "{name}" is already registered.')

        self._factories[name] = factory
