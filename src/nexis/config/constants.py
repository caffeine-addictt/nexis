"""
This file is for storing all the constants used in the project.
"""

import os
from typing import Literal, Tuple
import platformdirs


# The name of the config file
CONFIG_SOURCE_NAME: str = "nexis.toml"

# The directories where the config file can be found
# The last one will take precedence
#
# List of tuples (path, make_if_not_exist)
CONFIG_SOURCES: list[Tuple[str, bool]] = [
    (platformdirs.user_config_dir("nexis", ensure_exists=True), True),
    (os.getcwd(), False),
]

# Types for config keys
# Loaded config is converted to a flat tree, joined with '.'.
CONFIG_KEY = Literal[
    "mode",  # dev or prod
    "version",  # version of the nexis
    # [network]
    "network.api_url",  # url of the nexis api
    # [development.network]
    "development.network.api_url",  # url of the nexis api
]


__all__ = ["CONFIG_SOURCES", "CONFIG_SOURCE_NAME", "CONFIG_KEY"]
