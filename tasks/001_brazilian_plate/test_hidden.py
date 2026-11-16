import pytest

from solution import is_valid_plate


@pytest.mark.parametrize("plate", [
    "ABC1234",      # old format
    "ABC1D23",      # Mercosul
    "abc1234",      # lowercase
    "abc1d23",      # lowercase Mercosul
    "ABC-1234",     # hyphen, old
    "ABC-1D23",     # hyphen, Mercosul
])
def test_valid(plate):
    assert is_valid_plate(plate) is True


@pytest.mark.parametrize("plate", [
    "",             # empty
    "AB1234",       # too short
    "ABCD1234",     # too long
    "AB12345",      # wrong letter/digit split
    "1BC1234",      # digit where a letter is required
    "ABC12D3",      # letter in the wrong position
    "ABC 1234",     # space
    "ABC--1234",    # double hyphen
    "AB-C1234",     # hyphen in the wrong place
    "ABC1234 ",     # trailing space
    "ÁBC1234",      # accented letter is not A-Z
    "ABC１２３４",   # full-width digits are not 0-9
])
def test_invalid(plate):
    assert is_valid_plate(plate) is False


@pytest.mark.parametrize("value", [None, 1234567, ["ABC1234"], b"ABC1234"])
def test_non_string_returns_false(value):
    assert is_valid_plate(value) is False
