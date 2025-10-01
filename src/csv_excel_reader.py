import csv
import os
from csv import DictReader

import pandas as pd
from pandas import DataFrame


def csv_reader(path: str) -> str | list[dict]:
    """
    Функция принимает путь до файла с csv-данными и возвращает список словарей по этим данным
    :param path: путь к файлу с csv-данными
    :return: список словарей
    """
    transactions: list[dict] = []
    try:
        if not os.path.exists(path):
            raise FileNotFoundError("Файл не найден")

        if not path.lower().endswith(".csv"):
            raise ValueError("Расширение файла не CSV")

        with open(path, "r", encoding="utf-8") as file:
            reader: DictReader = csv.DictReader(file)
            for row in reader:
                transactions.append(row)

            return transactions

    except FileNotFoundError as ex:
        return f"{ex}"
    except ValueError as ex:
        return f"{ex}"
    except Exception as ex:
        return f"Произошла ошибка: {ex}"


def excel_reader(path: str) -> str | list[dict]:
    """
    Функция принимает путь до excel файла с данными, возвращает список словарей.
    :param path: Путь к excel файлу
    :return: список словарей
    """
    try:
        if not os.path.exists(path):
            raise FileNotFoundError("Файл не найден")

        if not path.lower().endswith(".xlsx"):
            raise ValueError("Расширение файла не xlsx")

        excel_data: DataFrame = pd.read_excel(path)
        transactions: list[dict] = excel_data.to_dict("records")

        return transactions

    except FileNotFoundError as ex:
        return f"{ex}"
    except ValueError as ex:
        return f"{ex}"
    except Exception as ex:
        return f"Произошла ошибка: {ex}"
