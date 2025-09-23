import json
import os.path
from typing import Union


def financial_transaction_data(datafile: str) -> Union[list, str]:
    """
    Функция принимает на вход путь до JSON-файла и возвращает список словарей с данными о финансовых транзакциях.
    Если файл пустой, содержит не список или не найден, функция возвращает пустой список
    """
    try:
        if not os.path.exists(datafile):
            raise FileNotFoundError([])

        if os.path.getsize(datafile) == 0:
            raise ValueError([])

        with open(datafile, "r", encoding="utf-8") as file:
            data: list = json.load(file)

            if not isinstance(data, list):
                raise TypeError([])

            return data

    except json.JSONDecodeError:
        return "Файл содержит невалидный JSON"
    except FileNotFoundError:
        return []
    except ValueError:
        return []
    except TypeError:
        return []
