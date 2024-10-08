from __future__ import annotations

import re

from nexis.config.exceptions import InvalidConfig
from nexis.config.parsers.parser import Parser


# Versioning pattern
# Following this project's Semantic Versioning spec and Python's PEP 440.
#
# https://peps.python.org/pep-0440/
VERSION_PATTERN = re.compile(
    r"""
    (?:
        (?:(?P<epoch>[0-9]+)!)?                           # epoch
        (?P<release>[0-9]+(?:\.[0-9]+)*)                  # release segment
        (?P<pre>                                          # pre-release
            [-_\.]?
            (?P<pre_l>(a|b|c|rc|alpha|beta|pre|preview))
            [-_\.]?
            (?P<pre_n>[0-9]+)?
        )?
        (?P<post>                                         # post release
            (?:-(?P<post_n1>[0-9]+))
            |
            (?:
                [-_\.]?
                (?P<post_l>post|rev|r)
                [-_\.]?
                (?P<post_n2>[0-9]+)?
            )
        )?
        (?P<dev>                                          # dev release
            [-_\.]?
            (?P<dev_l>dev)
            [-_\.]?
            (?P<dev_n>[0-9]+)?
        )?
    )
    (?:\+(?P<local>[a-z0-9]+(?:[-_\.][a-z0-9]+)*))?       # local version
""",
    re.VERBOSE | re.IGNORECASE,
)


class VersionParser(Parser):
    def _parse(self, value: str) -> str:
        # Strip leading v
        value = value.lstrip("v")
        if VERSION_PATTERN.fullmatch(value) is None:
            raise InvalidConfig(f"Invalid version string: {value}")
        return value
