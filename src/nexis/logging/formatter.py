from __future__ import annotations

import logging
from typing import ClassVar
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from logging import LogRecord


class IOFormatter(logging.Formatter):
    _colors: ClassVar[dict[str, str]] = {
        "error": "fg=red",
        "warning": "fg=yellow",
        "debug": "debug",
        "info": "fg=blue",
    }

    def format(self, record: LogRecord) -> str:
        if not record.exc_info:
            level = record.levelname.lower()
            msg = record.msg

            if level in self._colors:
                msg = f"<{self._colors[level]}>{msg}</>"

            record.msg = msg

        formatted = super().format(record)

        return formatted
