from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING, Optional

from cleo.io.null_io import NullIO

from nexis.config.config import Config
from nexis.config.constants import CONFIG_SOURCE_NAME, CONFIG_SOURCES
from nexis.nexis import Nexis
from nexis.version import __version__

if TYPE_CHECKING:
    from cleo.io.io import IO

    from nexis.nexis import Nexis


class Factory:
    """
    Factory class to create stuff needed by nexis.
    """

    def create_nexis(self, io: Optional[IO] = None) -> Nexis:
        """
        To initialize Nexis class and load config.
        """

        # Ensure I/O
        if io is None:
            io = NullIO()

        # Default nexis config
        config = Config(
            raw={
                "version": f"{__version__}",
                "mode": "dev",
                "network.api_url": "http://localhost:3000",
                "development.network.api_url": "http://localhost:3000",
            },
        )

        ptr = 0
        counter = 0
        while ptr < len(CONFIG_SOURCES):
            sourceDir, make = CONFIG_SOURCES[ptr]
            source = os.path.join(sourceDir, CONFIG_SOURCE_NAME)

            try:
                sourceConfig = Config(source)
                logging.debug(f"Loading config at {source}...")
                sourceConfig.load()
                config.merge(sourceConfig)

                counter += 1
                logging.debug(f"Loaded config at {source}...")

            except Exception as e:
                logging.debug(f"Config not found at {source}: {e}")
                if make:
                    logging.debug(f"Creating config at {source}...")

                    # Write new config
                    newConfig = Config(
                        path=source,
                        raw={
                            "version": f"{__version__}",
                            "mode": "dev",
                            "network.api_url": "http://localhost:3000",
                            "development.network.api_url": "http://localhost:3000",
                        },
                    )
                    newConfig.write()
                    io.write_line(f"<info>Config created at {source}...</>")

                    config.merge(newConfig)
                    counter += 1

            ptr += 1

        if counter == 0:
            raise FileNotFoundError(f"No config found at {CONFIG_SOURCES}")

        # Ensure config is valid
        logging.debug("Verifying config...")
        config.verify("throw")

        # Warn on version incompatibility
        if config.get("version") != __version__:
            logging.warning(
                f'Config version {config.get("version")} is different from the installed Nexis version {__version__}.'
                f' This may cause unintended behaviour.'
            )
            logging.warning(
                'You can update nexis by running "pip install --upgrade nexis".\n'
            )

        return Nexis(config)
