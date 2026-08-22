import pytest


def test_iterator_fails_gracefully():
    foo = []
    with pytest.raises(StopIteration):
        bar = next(foo)