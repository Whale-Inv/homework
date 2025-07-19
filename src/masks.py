def get_mask_card_number(card_number: int) -> str:
    """Функция, которая маскирует часть номера карты
    :rtype: str
    """

    string: str = str(card_number)
    masked_card_number: list[str] = []

    for i in range(0, len(string), 4):
        masked_card_number.append(string[i : i + 4])

    masked_card_number[1] = masked_card_number[1][:2] + "**"
    masked_card_number[2] = "****"
    result: str = " ".join(masked_card_number)

    return result


def get_mask_account(account_number: str) -> str:
    """Функция, которая маскирует номер счета"""

    string: str = str(account_number)
    masked_account: str = "**" + string[-4:]

    return masked_account
