from __future__ import annotations

import re

from nexis.config.exceptions import InvalidConfig
from nexis.config.parsers.parser import Parser


# URL pattern
URL_PATTERN = re.compile(
    r"""
    (?:http)s?://                                                                     # http:// or https://
    (?:                                                                               # domain
        (?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)
        |localhost
        |\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}                                           # ipv4
        |\[?[A-F0-9]*:[A-F0-9:]+\]?                                                   # ipv6
    )
    (?::\d+)?                                                                         # optional port
    (?:/?|[/?]\S+)
""",
    re.VERBOSE | re.IGNORECASE,
)


class URLParser(Parser):
    def _parse(self, value: str) -> str:
        if URL_PATTERN.fullmatch(value) is None:
            raise InvalidConfig(f"Invalid url string: {value}")
        return value
