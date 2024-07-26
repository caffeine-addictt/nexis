import logging
from cleo.io.io import IO


class IOHandler(logging.Handler):
    _io: IO

    def __init__(self, io: IO) -> None:
        self._io = io
        super().__init__()

    def emit(self, record: logging.LogRecord) -> None:
        try:
            msg = self.format(record)
            level = record.levelname.lower()
            err = level in ("warning", "error", "exception", "critical")
            if err:
                self._io.write_error_line(msg)
            else:
                self._io.write_line(msg)
        except Exception:
            self.handleError(record)
