from __future__ import annotations
import logging

from nexis.config.parsers.parser import Parser


class ModeParser(Parser):
    def _parse(self, value: str) -> str:
        value = value.strip().lower()
        if value in ["dev", "prod"]:
            return value

        logging.warning(f"{value} is not a valid mode, defaulting to prod")
        return "prod"
