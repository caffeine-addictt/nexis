from __future__ import annotations
from typing import Any

from nexis.config.constants import CONFIG_KEY
from nexis.config.parsers.mode import ModeParser
from nexis.config.parsers.parser import Parser
from nexis.config.parsers.url import URLParser
from nexis.config.parsers.version import VersionParser


class Parsers(dict[CONFIG_KEY, Parser]):
    """
    A class that holds all parsers.
    """

    def __init__(self, *parsers: Parser) -> None:
        """
        Initializes the parsers.

        Parameters
        ----------
        :param parsers: The parsers to add
        """
        super().__init__()
        for parser in parsers:
            for key in parser.key:
                self[key] = parser

    def parse(self, key: CONFIG_KEY, value: Any) -> Any:
        """
        Parses a config value.

        Parameters
        ----------
        :param key: The key to parse
        :param value: The config value to parse

        Returns
        -------
        :return: The parsed config value

        Raises
        ------
        :raises InvalidConfig: If the config value is invalid
        """
        return self[key].parse(value) if key in self else value


DEFAULT_PARSERS = Parsers(
    ModeParser(["mode"]),
    URLParser(["network.api_url", "development.network.api_url"]),
    VersionParser(["version"]),
)
