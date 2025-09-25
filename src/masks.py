import logging
from logging import Formatter, Handler, Logger

logger: Logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)
file_handler: Handler = logging.FileHandler("logs/masks.log", mode="w", encoding="utf-8")
file_formatter: Formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: int | str) -> str:
    """Функция, которая маскирует часть номера карты
    :rtype: str
    """
    logger.info(f"Проверяем является ли {card_number} целым числом, длиной 16 цифр")
    if isinstance(card_number, int) and (16 >= len(str(card_number)) > 15):
        string: str = str(card_number)
        masked_card_number: list[str] = []

        logger.info("Выполняем маскировку номера карты")
        for i in range(0, len(string), 4):
            masked_card_number.append(string[i : i + 4])

        masked_card_number[1] = masked_card_number[1][:2] + "**"
        masked_card_number[2] = "****"
        result: str = " ".join(masked_card_number)

        return result
    else:
        logger.error("Введен некорректный номер карты")
        return "некорректный номер карты"


def get_mask_account(account_number: int | str) -> str:
    """Функция, которая маскирует номер счета"""
    logger.info(f"Проверяем является ли {account_number} целым числом длиной 20 цифр")
    if isinstance(account_number, int) and (20 >= len(str(account_number)) > 19):
        string: str = str(account_number)
        logger.info("Выполняем маскировку номера счета")
        masked_account: str = "**" + string[-4:]

        return masked_account
    else:
        logger.error("Введен некорректный номер счета")
        return "некорректный номер счета"
