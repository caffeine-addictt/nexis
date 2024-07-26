from __future__ import annotations

from abc import abstractmethod
from typing import Any, Iterable, Optional, Union, overload, TYPE_CHECKING
from typing_extensions import Generic, TypeVar

from nexis.config.exceptions import InvalidConfig

if TYPE_CHECKING:
    from nexis.config.constants import CONFIG_KEY


_T = TypeVar("_T")
_DEFAULT_T = TypeVar("_DEFAULT_T")


class Parser(Generic[_T]):
    """
    A parser class to parse a single config value.
    """

    key: Iterable[CONFIG_KEY]
    default: Optional[_T]

    def __init__(self, key: Iterable[CONFIG_KEY], default: Optional[_T] = None) -> None:
        """
        Initializes the parser.

        Parameters
        ----------
        :param key: The key to parse
        :param default: The default value to return if the config value is invalid
        """
        self.key = key
        self.default = default

    @abstractmethod
    def _parse(self, value: Any) -> Union[Any, _T]:
        """
        Parses a single config value.

        Parameters
        ----------
        :param value: The config value to parse

        Returns
        -------
        :return: The parsed config value
        """
        raise NotImplementedError()

    @overload
    def parse(self, value: Any) -> Union[Any, _T]: ...

    @overload
    def parse(self, value: Any, default: _DEFAULT_T) -> Union[Any, _T, _DEFAULT_T]: ...

    def parse(
        self, value: Any, default: Optional[_DEFAULT_T] = None
    ) -> Union[Any, _DEFAULT_T, _T]:
        """
        Parses a single config value.

        Parameters
        ----------
        :param value: The config value to parse
        :param default: The default value to return if the config value is invalid (overrides `self.default`)

        Returns
        -------
        :return: The parsed config value
        """
        try:
            return self._parse(value)
        except Exception as e:
            if default is None:
                raise InvalidConfig(
                    f"{value} is not a valid config value for {self.key}"
                ) from e
            return default
