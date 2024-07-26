# Ensure that resolving version does not error


def test_version():
    from nexis import __version__

    assert __version__, "Nexis version should be defined"
