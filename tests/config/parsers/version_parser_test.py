import pytest
from typing import Optional

from nexis.config.exceptions import InvalidConfig
from nexis.config.parsers import version


@pytest.mark.parametrize(
    "ver,expected",
    [
        ("0.0.0", "0.0.0"),
        ("0.0.1", "0.0.1"),
        ("0.1.0", "0.1.0"),
        ("0.1.1", "0.1.1"),
        ("1.0.0", "1.0.0"),
        ("1.0.1", "1.0.1"),
        ("1.1.0", "1.1.0"),
        ("1.1.1", "1.1.1"),
        ("2.0.0", "2.0.0"),
        ("2.0.1", "2.0.1"),
        ("2.1.0", "2.1.0"),
        ("2.1.1", "2.1.1"),
        ("3.0.0", "3.0.0"),
        ("1.0.0-alpha.1", "1.0.0-alpha.1"),
        ("1.0.0-beta.2", "1.0.0-beta.2"),
        ("1.0.0-rc.3", "1.0.0-rc.3"),
        ("1.0.0-a.23", "1.0.0-a.23"),
        ("1.0.0-b.23", "1.0.0-b.23"),
        ("1.0.0-dev.23", "1.0.0-dev.23"),
        ("1.0.0-rc.2-dev.23", "1.0.0-rc.2-dev.23"),
        ("1.0.0-rc.2+dev.23", "1.0.0-rc.2+dev.23"),
        # Leading v is stripped
        ("v1.0.0", "1.0.0"),
        ("v1.0.0-alpha.1", "1.0.0-alpha.1"),
        ("v1.0.0-beta.2", "1.0.0-beta.2"),
        ("v1.0.0-rc.3", "1.0.0-rc.3"),
        ("v1.0.0-a.23", "1.0.0-a.23"),
        ("v1.0.0-b.23", "1.0.0-b.23"),
        ("v1.0.0-dev.23", "1.0.0-dev.23"),
        ("v1.0.0-rc.2-dev.23", "1.0.0-rc.2-dev.23"),
        ("v1.0.0-rc.2+dev.23", "1.0.0-rc.2+dev.23"),
        ("v0.0.0", "0.0.0"),
        ("v0.0.1", "0.0.1"),
        ("v0.1.0", "0.1.0"),
        ("v0.1.1", "0.1.1"),
        ("v2.0.0", "2.0.0"),
        ("v2.0.1", "2.0.1"),
        ("v2.1.0", "2.1.0"),
        ("v2.1.1", "2.1.1"),
        ("v3.0.0", "3.0.0"),
    ],
)
def test_version_pattern(ver, expected: Optional[str]):
    assert version.VersionParser(["version"]).parse(ver) == expected


@pytest.mark.parametrize(
    "ver",
    [
        "sdawdawd",
        "sadwda",
        "1.0.0-alpha.1-beta.2",
        "1.0.0-alpha.1-beta.2-rc.3",
        "1.0.0-alpha.1-beta.2-rc.3+build.4",
        "1.0.0-alpha.1-beta.2-rc.3+build.4-with-suffix",
        "1.0.0-0.3.7-beta.2-rc.3+build.4-with-suffix",
        "1.0.0-0.3.7-beta.2-rc.3+build.4-with-suffix.5",
        "1.0.0-0.3.7",
        "1.0.0-0.3.7-0.4.7",
        "1.0.0-0.3.7-0.4.7-0.5.7",
        "1.0.0-0.3.7-0.4.7-0.5.7-0.6.7",
    ],
)
def test_version_pattern_invalid(ver):
    with pytest.raises(InvalidConfig):
        version.VersionParser(["version"]).parse(ver)
