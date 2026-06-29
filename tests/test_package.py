from rockmicro import __version__


def test_package_has_version():
    assert __version__ != "0+unknown"


def test_legacy_package_is_lazy():
    import Scripts

    assert Scripts.moose.__name__ == "rockmicro.moose"
