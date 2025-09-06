def get_mask_card_number(card_number: int | str) -> str:
    """Функция, которая маскирует часть номера карты
    :rtype: str
    """
    if isinstance(card_number, int) and (16 >= len(str(card_number)) > 15):
        string: str = str(card_number)
        masked_card_number: list[str] = []

        for i in range(0, len(string), 4):
            masked_card_number.append(string[i : i + 4])

        masked_card_number[1] = masked_card_number[1][:2] + "**"
        masked_card_number[2] = "****"
        result: str = " ".join(masked_card_number)

        return result
    else:
        return "некорректный номер карты"


def get_mask_account(account_number: int | str) -> str:
    """Функция, которая маскирует номер счета"""

    if isinstance(account_number, int) and (20 >= len(str(account_number)) > 19):
        string: str = str(account_number)
        masked_account: str = "**" + string[-4:]

        return masked_account
    else:
        return "некорректный номер счета"
