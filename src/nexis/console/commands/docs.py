import webbrowser
from cleo.helpers import option

from nexis.console.commands.command import Command
from nexis.version import __version__


class DocsCommand(Command):
    """
    The docs command

    1. StdOut docs url
    2. Open new browser tab (Opt-Out)
    """

    name = "docs"
    description = "Go to the documentation!"
    options = [
        option(
            "browserless", "B", "If set, the docs will not be opened in the browser"
        ),
    ]

    def _handle(self) -> int:
        branch = "main" if self.option("dev") else f"v{__version__}"
        url = f"https://github.com/caffeine-addictt/nexis/blob/{branch}/docs/README.md"
        resp = f"<info>{url}</info>"

        if not self.option("browserless"):
            webbrowser.open_new_tab(url)
            resp = f"Opening {resp} in your browser..."

        self.line(resp)
        return 0
