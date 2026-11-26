"""Unit tests for vitalx.quotes (quote retrieval).

What to test:
- get_random_quote returns a string
- The returned string is one of the quotes in the QUOTES list
- The QUOTES list is non-empty
- get_random_quote returns different quotes on multiple calls (probabilistic - run many times)
- The return type is str

Suggested mocks:
- Mock random.choice to return a specific quote for deterministic testing
"""

import random
from vitalx.quotes import get_random_quote, QUOTES


def test_get_random_quote_returns_string():
    """
    get_random_quote() should return a str.
    Hint: assert isinstance(result, str).
    """
    pass


def test_get_random_quote_is_from_quotes_list():
    """
    The returned quote should be one of the strings in the QUOTES list.
    Hint: assert result in QUOTES.
    """
    pass


def test_quotes_list_is_non_empty():
    """
    QUOTES should contain at least one quote.
    Hint: assert len(QUOTES) > 0.
    """
    pass


def test_get_random_quote_returns_different_values_over_many_calls():
    """
    Over many calls, get_random_quote should return a variety of quotes.
    This is probabilistic - call it 100 times and assert you get more than one
    unique result (unless QUOTES only has one entry).
    Hint: use a set to collect unique results.
    """
    pass


def test_get_random_quote_mocked(monkeypatch):
    """
    Mock random.choice to make the test deterministic.
    Hint: monkeypatch random.choice to always return the first quote,
    then assert get_random_quote() == QUOTES[0].
    """
    pass
