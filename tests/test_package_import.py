def test_package_can_be_imported() -> None:
    import atlas_core

    assert atlas_core.__version__ == "0.1.0"
