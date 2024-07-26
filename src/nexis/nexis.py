from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from nexis.config.config import Config


class Nexis:
    """
    Used to persist state
    """

    _config: Config

    def __init__(self, config: Config) -> None:
        """
        Initializes Nexis

        Parameters
        ----------
        :param config: The config to use
        """
        self._config = config

    @property
    def config(self) -> Config:
        """The loaded configuration, READ-ONLY"""
        return self._config
