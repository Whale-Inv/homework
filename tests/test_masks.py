from typing import Callable

import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "card_number, mask_card_number",
    [(7000792289606361, "7000 79** **** 6361"), (4000123456789012, "4000 12** **** 9012")],
)
def test_get_mask_card_number(card_number: int, mask_card_number: str) -> None:
    assert get_mask_card_number(card_number) == mask_card_number


def test_get_mask_card_number_incorrect(incorrect_card_number: Callable[[], str]) -> None:
    assert get_mask_card_number(1) == incorrect_card_number

    assert get_mask_card_number(21) == incorrect_card_number

    assert get_mask_card_number(" ") == incorrect_card_number

    assert get_mask_card_number(12345678901234567) == incorrect_card_number

    assert get_mask_card_number("123b019231023129") == incorrect_card_number


@pytest.mark.parametrize("account, mask_account", [(73654108430135874305, "**4305"), (43013587430573654108, "**4108")])
def test_get_mask_account(account: int, mask_account: str) -> None:
    assert get_mask_account(account) == mask_account


def test_get_mask_account_incorrect(incorrect_account_number: Callable[[], str]) -> None:
    assert get_mask_account(1) == incorrect_account_number

    assert get_mask_account(123) == incorrect_account_number

    assert get_mask_account(" ") == incorrect_account_number

    assert get_mask_account("1239292g291923as") == incorrect_account_number
