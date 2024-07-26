import pytest

from nexis.config.parsers import mode


@pytest.mark.parametrize(
    "m,expected",
    [
        ("prod", "prod"),
        ("dev", "dev"),
        ("PROD", "prod"),
        ("DEV", "dev"),
        ("PrOD", "prod"),
        ("DeV", "dev"),
        # Default to prod
        ("", "prod"),
        ("production", "prod"),
        ("sdewfefes", "prod"),
        ("invalid", "prod"),
        ("prod1", "prod"),
    ],
)
def test_mode_pattern(m, expected):
    assert mode.ModeParser(["mode"]).parse(m) == expected
