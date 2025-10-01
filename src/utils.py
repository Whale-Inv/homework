import json
import os.path
import re
from typing import Any, Union

from black.trans import defaultdict


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


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """
    Функция принимает список словарей с данными о банковских операциях и строку поиска,
    а возвращает список словарей, у которых в описании есть данная строка.
    """
    try:
        if not isinstance(data, list):
            raise TypeError("Параметр data должен быть списком")
        if not isinstance(search, str):
            raise TypeError("Параметр search должен быть строкой")

        try:
            regex: re.Pattern[str] = re.compile(search)
        except re.error as e:
            raise ValueError(f"Ошибка в регулярном выражении: {str(e)}")

        results: list[dict] = []

        for operation in data:
            try:
                if not isinstance(operation, dict):
                    raise ValueError("Элемент списка data не является словарем")

                for key, value in operation.items():
                    if isinstance(value, str):
                        if regex.findall(value):
                            results.append(operation)
                            break

            except Exception as ex:
                print(f"Ошибка при обработке операции {operation}: {str(ex)}")

        return results

    except Exception as ex:
        print(f"Критическая ошибка при поиске: {str(ex)}")
        return []


def process_bank_operations(data: list[dict], categories: list) -> dict:
    """
    Функция принимает список словарей с данными о банковских операциях и список категорий операций,
    а возвращает словарь, в котором ключи — это названия категорий,
    а значения — это количество операций в каждой категории.
    """
    try:
        if not isinstance(data, list):
            raise TypeError("Параметр data должен быть списком")
        if not isinstance(categories, list):
            raise TypeError("Параметр categories должен быть списком")

        category_counts: defaultdict = defaultdict(int, {category: 0 for category in categories})

        for operation in data:
            try:
                if not isinstance(operation, dict):
                    raise ValueError("Элемент списка data не является словарем")

                category: Any = operation.get("description")

                if category is None:
                    raise KeyError("В операции отсутствует ключ 'description'")

                if not isinstance(category, str):
                    raise TypeError("Категория должна быть строкой")

                if category in categories:
                    category_counts[category] += 1
                else:
                    print(f"Предупреждение: категория '{category}' не найдена в списке допустимых категорий")

            except Exception as ex:
                print(f"Ошибка при обработке операции {operation}: {str(ex)}")

        return dict(category_counts)

    except Exception as ex:
        print(f"Критическая ошибка при обработке данных: {str(ex)}")
        return {}
