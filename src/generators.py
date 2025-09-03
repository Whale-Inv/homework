from typing import Generator


def filter_by_currency(transactions: list, currency: str = "USD") -> list:
    return list(filter(lambda x: x["operationAmount"]["currency"]["code"] == currency, transactions))


def transaction_descriptions(transactions: list) -> Generator:
    for transaction in transactions:
        yield transaction["description"]


def card_number_generator(start: int, stop: int) -> Generator:

    if not isinstance(start, int) or not isinstance(stop, int):
        raise TypeError("Номер карты может содержать только числовые значения")

    if start > stop:
        raise ValueError("Начальное значение должно быть меньше конечного")

    while start <= stop:
        num_str: str = f"{start:016d}"
        formatted_card_number: str = " ".join(num_str[i : i + 4] for i in range(0, 16, 4))

        yield formatted_card_number
        start += 1
