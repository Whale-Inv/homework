from datetime import datetime
from typing import Any

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(card: str) -> str:
    # Функция, которая маскирует номер счета и номер карты
    split_card: list[str] = card.split()
    type_card:list[str] = ["Visa", "MasterCard", "Maestro"]

    for card_types in type_card:
        if card_types in card:
            for elem in split_card:
                if elem.isdigit():
                    card_number: Any = elem
                    split_card.pop()
                    split_card.append(get_mask_card_number(card_number))

        elif "Счет" in card:
            for elem in split_card:
                if elem.isdigit():
                    card_number = elem
                    split_card.pop()
                    split_card.append(get_mask_account(card_number))

    return " ".join(split_card)


def get_date(date_str: str) -> str:
    # Функция, которая приводит дату к нужному формату
    date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
    return date.strftime("%d.%m.%Y")

print(mask_account_card("Visa Platinum 8990922113665229"))