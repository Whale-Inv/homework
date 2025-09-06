from typing import Callable

import pytest
from pytest import raises

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "value, expected",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Maestro 7000792289606361", "Maestro 7000 79** **** 6361"),
        ("Счет 73654108430135874305", "Счет **4305"),
    ],
)
def test_mask_account_card(value: str, expected: str) -> None:
    assert mask_account_card(value) == expected


def test_mask_account_card_incorrect(incorrect_account_card: Callable[[], str]) -> None:
    assert mask_account_card(11) == incorrect_account_card

    assert mask_account_card(" ") == incorrect_account_card

    assert mask_account_card("aasdfqwer") == incorrect_account_card


@pytest.mark.parametrize(
    "date, format_date",
    [
        ("2025-08-24T12:34:56.123", "24.08.2025"),
        ("2025-01-01T00:00:00.000", "01.01.2025"),
        ("2025-12-31T23:59:59.999", "31.12.2025"),
    ],
)
def test_get_date(date: str, format_date: str) -> None:
    assert get_date(date) == format_date

    assert get_date(date) == format_date

    assert get_date(date) == format_date


def test_get_date_error() -> None:

    with raises(ValueError):
        get_date("24.08.2025")

    with raises(ValueError):
        get_date("2025/08/24T12:34:56.123")

    with raises(ValueError):
        get_date("2025-02-30T12:34:56.123")

    with raises(ValueError):
        get_date("2025-13-01T12:34:56.123")

    with raises(ValueError):
        get_date("")
