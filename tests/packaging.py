"""Tests around project's packaging."""
import odooselenium


def test_version():
    """``odooselenium.__version__`` shows software version."""
    assert odooselenium.__version__
