import pytest

from nexis.config.exceptions import InvalidConfig
from nexis.config.parsers import url


@pytest.mark.parametrize(
    "v",
    [
        # localhost
        "http://localhost:3000",
        "http://localhost:3000/with/path",
        "http://localhost:3000/with/path?query=1",
        "http://localhost:3000/with/path#fragment",
        # domain
        "https://ngjx.org",
        "https://ngjx.org/with/path",
        "https://ngjx.org/with/path?query=1",
        "https://ngjx.org/with/path#fragment",
        # ipv4
        "http://1.1.1.1:3000",
        "http://1.1.1.1:3000/with/path",
        "http://1.1.1.1:3000/with/path?query=1",
        "http://1.1.1.1:3000/with/path#fragment",
        # ipv6 abbrev
        "http://[fd::1]:3000",
        "http://[f24::1]:3000/with/path",
        "http://[::df]:3000/with/path?query=1",
        "http://[::1]:3000/with/path#fragment",
        # ipv6 full
        "http://[2b5b:1e49:8d01:c2ac:fffd:833e:dfee:13a4]:3000",
        "http://[::c2ac:fffd:833e:dfee:13a4]:3000/with/path",
        "http://[2b5b:1e49::dfee:13a4]:3000/with/path?query=1",
        "http://[2b5b:1e49:8d01:c2ac:fffd::]:3000/with/path#fragment",
    ],
)
def test_url_pattern(v):
    assert url.URLParser(["network.api_url"]).parse(v) == v


@pytest.mark.parametrize(
    "v",
    [
        "ewfwefw",
        "httttp://a.a.a",
        "http://[ffffffffffff::].com",
        "localhost",
        "localhost:3232",
        "ngjx.org",
    ],
)
def test_url_pattern_invalid(v):
    with pytest.raises(InvalidConfig):
        url.URLParser(["network.api_url"]).parse(v)
