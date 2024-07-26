from __future__ import annotations

from typing import TYPE_CHECKING, Optional
from typing import Any
from typing import ClassVar

from cleo.commands.command import Command as BaseCommand
from cleo.exceptions import CleoValueError

from nexis.nexis import Nexis


if TYPE_CHECKING:
    from nexis.console.entrypoint import Application


class Command(BaseCommand):
    """
    Base class for all NEXIS commands.

    To use this class, subclass it and implement the `_handle` method.
    The `name` property should be set to the command name.

    Usage
    -----
    ```py
    class MyCmd(Command):
        name = "mycmd"

        def _handle(self) -> int:
            return 0
    ```
    """

    loggers: ClassVar[list[str]] = []

    _nexis: Optional[Nexis] = None
    """Do not use this directly. Use `self.nexis` instead."""

    skip_pre_load_config: bool = False
    """Set this to True if you want to skip the pre-load config step."""

    @property
    def nexis(self) -> Nexis:
        if not self._nexis:
            self._nexis = self.get_application().nexis
        return self._nexis

    def _handle(self) -> int:
        raise NotImplementedError()

    def handle(self) -> int:
        """Do not override this method, use `_handle` instead."""

        if not self.skip_pre_load_config:
            self._nexis = self.get_application().nexis
        return self._handle()

    def get_application(self) -> Application:
        from nexis.console.entrypoint import Application

        application = self.application
        assert isinstance(application, Application)
        return application

    def option(self, name: str, default: Any = None) -> Any:
        try:
            return super().option(name)
        except CleoValueError:
            return default
