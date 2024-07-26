from __future__ import annotations

import os
from pathlib import Path
import tomllib
from typing import Any, Literal, Tuple, Union, TYPE_CHECKING
from typing_extensions import TypeVar, cast

from nexis.config.exceptions import InvalidConfig

if TYPE_CHECKING:
    from nexis.config.constants import CONFIG_KEY


_T = TypeVar("_T")
JOINS = Literal[
    "outer left",
    "outer right",
    "full outer",
    "inner",
]


class Config:
    path: Union[str, Path, None]
    raw: dict[CONFIG_KEY, str]

    def __init__(
        self,
        path: Union[str, Path, None] = None,
        raw: Union[dict[CONFIG_KEY, str], None] = None,
    ) -> None:
        self.path = path
        self.raw = {} if raw is None else raw

    def get(self, key: CONFIG_KEY, default: _T = None) -> Union[_T, Any]:
        """
        Get a value from the config

        Parameters
        ----------
        :param key: The key to get
        :param default: The default value to return if the key doesn't exist
        """
        return self.raw.get(key, default)

    def add(self, key: CONFIG_KEY, value: Any) -> None:
        """
        Add a new key/value pair to the config

        Parameters
        ----------
        :param key: The key to add
        :param value: The value to add
        """
        self.raw[key] = value

    def remove(self, key: CONFIG_KEY) -> None:
        """
        Remove a key from the config

        Parameters
        ----------
        :param key: The key to remove
        """
        self.raw.pop(key, None)

    def merge(self, config: Config, join: JOINS = "full outer") -> None:
        """
        Merge another config into this one.

        Parameters
        ----------
        :param config: The config to merge
        :param join: The type of join to perform
        """
        match join:
            case "outer right":
                self.raw.update(
                    {
                        k: new
                        for k, v in config.raw.items()
                        if (new := self.raw.get(k, v)) and (new != v)
                    }
                )
            case "outer left":
                self.raw.update(
                    {
                        k: new
                        for k, v in self.raw.items()
                        if (new := config.raw.get(k, v)) and (new != v)
                    }
                )
            case "full outer":
                self.raw.update(config.raw)
            case "inner":
                keys = set(config.raw.keys()) & set(self.raw.keys())
                self.raw = {k: config.raw[k] for k in keys}
            case _:
                raise ValueError(f"Invalid join: {join}")

    def load(self) -> None:
        """
        Load the config from the path
        """
        assert self.path, "Path not set"
        assert os.path.isfile(self.path), f"File not found: {self.path}"
        from nexis.config.constants import CONFIG_KEY

        with open(self.path, "rb") as f:
            data = tomllib.load(f)

        self.raw = cast(dict[CONFIG_KEY, str], self.flatten(data))
        self.verify("remove")

    def write(self) -> None:
        """
        Write the config to the path

        Raises
        ------
        AssertionError: If the path is not set
        """
        assert self.path, "Path not set, cannot write config"

        with open(self.path, "w") as f:
            f.write(self.marshal())

    def verify(self, mode: Literal["throw", "remove"] = "remove") -> None:
        """
        Verify the config
        [0(n) space and time]

        Parameters
        ----------
        :param mode: The mode to use when there is an invalid key
        """
        assert mode in ("throw", "remove"), f"Invalid mode: {mode}"
        from nexis.config.constants import CONFIG_KEY
        from nexis.config.parsers.parsers import DEFAULT_PARSERS

        allow_key = set(CONFIG_KEY.__dict__["__args__"])  # use set for 0(1) lookup

        # Create a shallow copy if i have to mutate `self.raw`
        # so that it will still be safe to iterate over it
        to_iter = self.raw.items() if mode == "throw" else list(self.raw.items())

        for k, v in to_iter:
            # handle key
            if k not in allow_key:
                if mode == "throw":
                    raise InvalidConfig(f"Invalid config: {k}")
                else:
                    del self.raw[k]
                    continue

            # handle value
            self.raw[k] = DEFAULT_PARSERS.parse(k, v)

    def flatten(self, data: dict[str, Any]) -> dict[str, Any]:
        """
        Flatten the config
        """
        flat = {}

        def _flatten(d: dict[str, Any], stack: list[str]) -> None:
            for k, v in d.items():
                if isinstance(v, dict):
                    _flatten(v, stack + [k])
                else:
                    flat[".".join(stack + [k])] = v

        _flatten(data, [])
        return flat

    def marshal(self) -> str:
        """
        Marshal the config into POSIX compliant TOML format.
        (AKA. LF endings, no trailing spaces and trailing newline)

        Returns
        -------
        :return: The config in TOML format
        """
        toplevel: list[Tuple[str, Any]] = []
        groups: dict[str, list[Tuple[str, Any]]] = {}

        def marshal_group(d: list[Tuple[str, Any]]) -> str:
            return "\n".join(f'{k} = "{v}"' for k, v in sorted(d))

        for k, v in self.raw.items():
            if "." not in k:
                toplevel.append((k, v))
            else:
                parts = k.split(".")
                key = ".".join(parts[:-1])
                groups[key] = groups.get(key, [])
                groups[key].append((parts[-1], v))

        marshalled = marshal_group(toplevel)

        if len(groups) > 0:
            marshalled += "\n\n"
            marshalled += "\n\n".join(
                f"[{group}]\n" + marshal_group(keyval)
                for group, keyval in groups.items()
            )

        return marshalled + "\n"
