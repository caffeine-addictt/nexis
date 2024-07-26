import logging
from pathlib import Path
from typing import Optional
from cleo.application import Application as BaseApplication
from cleo.events.console_command_event import ConsoleCommandEvent
from cleo.events.console_events import COMMAND
from cleo.events.event import Event
from cleo.events.event_dispatcher import EventDispatcher
from cleo.formatters.style import Style
from cleo.io.inputs.definition import Definition
from cleo.io.inputs.input import Input
from cleo.io.inputs.option import Option
from cleo.io.io import IO
from cleo.io.outputs.output import Output

from nexis.config.constants import CONFIG_SOURCE_NAME, CONFIG_SOURCES
from nexis.console.command_loader import COMMANDS, CommandLoader, load_command
from nexis.console.commands.command import Command
from nexis.factory import Factory
from nexis.logging.formatter import IOFormatter
from nexis.logging.handler import IOHandler
from nexis.nexis import Nexis
from nexis.version import __version__


class Application(BaseApplication):
    _nexis: Optional[Nexis]
    _io: Optional[IO]

    def __init__(self) -> None:
        super().__init__(name="Nexis", version=__version__)

        self._io = None
        self._nexis = None

        dispatcher = EventDispatcher()
        dispatcher.add_listener(COMMAND, self.register_loggers)
        self.set_event_dispatcher(dispatcher)

        self.set_command_loader(
            CommandLoader({name: load_command(name) for name in COMMANDS})
        )

    @property
    def nexis(self) -> Nexis:
        # Check if already exists
        if self._nexis is not None:
            return self._nexis

        # Update SOURCES
        if self._io is not None and self._io.input.option("config"):
            CONFIG_SOURCES.append(
                (
                    Path(self._io.input.option("config")).absolute().as_posix(),
                    False,
                )
            )

        self._nexis = Factory().create_nexis(self._io)
        return self._nexis

    def create_io(
        self,
        input: Optional[Input] = None,
        output: Optional[Output] = None,
        error_output: Optional[Output] = None,
    ) -> IO:
        io = super().create_io(input, output, error_output)

        formatter = io.output.formatter
        formatter.set_style("c1", Style("cyan"))
        formatter.set_style("c2", Style("default", options=["bold"]))
        formatter.set_style("info", Style("blue"))
        formatter.set_style("comment", Style("green"))
        formatter.set_style("warning", Style("yellow"))
        formatter.set_style("debug", Style("default", options=["dark"]))
        formatter.set_style("success", Style("green"))

        io.output.set_formatter(formatter)
        io.error_output.set_formatter(formatter)

        self._io = io
        return io

    @property
    def _default_definition(self) -> Definition:
        """Overriding BaseApplication's default definition so I can add global options/flags."""

        definition = super()._default_definition
        definition.add_options(
            [
                Option(
                    "--dev",
                    "-D",
                    description=f"Use development options defined in <info>{CONFIG_SOURCE_NAME}</info>.",
                ),
                Option(
                    "--config",
                    "-C",
                    flag=False,
                    description="Use the specified configuration file.",
                ),
            ]
        )

        return definition

    def register_loggers(self, event: Event, *_) -> None:
        assert isinstance(event, ConsoleCommandEvent)

        if not isinstance(event.command, Command):
            return

        handler = IOHandler(event.io)
        handler.setFormatter(IOFormatter())

        level = logging.WARNING
        if event.io.is_debug():
            level = logging.DEBUG
        elif event.io.is_very_verbose() or event.io.is_verbose():
            level = logging.INFO

        logging.basicConfig(level=level, handlers=[handler])


def main() -> int:
    return Application().run()


if __name__ == "__main__":
    main()
