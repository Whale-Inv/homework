import json
import logging
import os.path
from logging import Formatter, Handler, Logger
from typing import Union

logger: Logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)
file_handler: Handler = logging.FileHandler("logs/utils.log", mode="w", encoding="utf-8")
file_formatter: Formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def financial_transaction_data(datafile: str) -> Union[list, str]:
    """
    Функция принимает на вход путь до JSON-файла и возвращает список словарей с данными о финансовых транзакциях.
    Если файл пустой, содержит не список или не найден, функция возвращает пустой список
    """
    try:
        logger.info("Проверяем существует ли файл по указанному пути и удается ли его найти")
        if not os.path.exists(datafile):
            raise FileNotFoundError([])

        logger.info("Проверяем является ли файл пустым")
        if os.path.getsize(datafile) == 0:
            raise ValueError([])

        logger.info("Открываем файл")
        with open(datafile, "r", encoding="utf-8") as file:
            data: list = json.load(file)

            logger.info("Проверяем содержит ли файл список")
            if not isinstance(data, list):
                raise TypeError([])

            return data

    except json.JSONDecodeError as ex:
        logger.error(f"Произошла ошибка {ex}")
        return "Файл содержит невалидный JSON"
    except FileNotFoundError as ex:
        logger.error(f"Произошла ошибка {ex}")
        return []
    except ValueError as ex:
        logger.error(f"Произошла ошибка {ex}")
        return []
    except TypeError as ex:
        logger.error(f"Произошла ошибка {ex}")
        return []
