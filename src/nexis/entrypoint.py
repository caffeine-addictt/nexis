from cleo.application import Application as BaseApplication

from nexis.version import __version__


class Application(BaseApplication):
    def __init__(self) -> None:
        super().__init__(name='Nexis', version=__version__)


def main() -> int:
    return Application().run()


if __name__ == '__main__':
    main()
