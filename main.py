import json
import os
from pprint import pprint
from typing import Any

from src.csv_excel_reader import csv_reader, excel_reader
from src.external_api import sum_from_transaction
from src.processing import filter_by_state, sort_by_date
from src.utils import process_bank_search


def main() -> None:
    """
    Основная функция программы для работы с банковскими транзакциями.

    Функция предоставляет пользователю интерфейс для:
    * Выбора типа файла с данными (JSON, CSV, XLSX)
    * Фильтрации операций по статусу (EXECUTED, CANCELED, PENDING)
    * Сортировки операций по дате
    * Фильтрации по валюте (только рубли)
    * Поисковой фильтрации по слову в описании операции

    Программа выполняет следующие действия:
    1. Определяет путь к файлам данных
    2. Предлагает выбрать тип файла для обработки
    3. Загружает данные из выбранного файла
    4. Проводит фильтрацию по статусу операции
    5. Выполняет сортировку по дате (опционально)
    6. Фильтрует операции по валюте (опционально)
    7. Проводит поисковую фильтрацию (опционально)
    8. Выводит итоговый список транзакций

    Параметры файлов:
    - JSON-файл: data/operations.json
    - CSV-файл: data/transactions.csv
    - XLSX-файл: data/transactions_excel.xlsx

    Доступные статусы операций:
    - EXECUTED
    - CANCELED
    - PENDING

    Возвращаемое значение: None
    Функция работает интерактивно через консоль и выводит результаты на экран.
    """
    current_dir: str = os.path.dirname(__file__)
    json_file_path: str = os.path.join(current_dir, "data", "operations.json")
    csv_file_path: str = os.path.join(current_dir, "data", "transactions.csv")
    xlsx_file_path: str = os.path.join(current_dir, "data", "transactions_excel.xlsx")

    file_type: int = int(
        input(
            """
    Привет! Добро пожаловать в программу работы с банковскими транзакциями.
Выберите необходимый пункт меню:
1. Получить информацию о транзакциях из JSON-файла
2. Получить информацию о транзакциях из CSV-файла
3. Получить информацию о транзакциях из XLSX-файла
    """
        )
    )

    if file_type in [1, 2, 3]:
        if file_type == 1:
            print("Для обработки выбран JSON-файл")
            with open(json_file_path, "r", encoding="utf-8") as file:
                data: Any = json.load(file)
                data_file: Any = data
        if file_type == 2:
            print("Для обработки выбран CSV-файл")
            data_file = csv_reader(csv_file_path)
        if file_type == 3:
            print("Для обработки выбран XLSX-файл")
            data_file = excel_reader(xlsx_file_path)

    user_input_status: str = input(
        """
    Введите статус, по которому необходимо выполнить фильтрацию.
Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING
    """
    ).upper()
    while True:
        if user_input_status in ["EXECUTED", "CANCELED", "PENDING"]:
            print(f'Операции отфильтрованы по статусу "{user_input_status}"')
            filtered_by_status: list[dict] = filter_by_state(data_file, user_input_status)
            break
        else:
            print(f'Статус операции "{user_input_status}" недоступен')
            continue

    user_input_sort: str = input("Отсортировать операции по дате? Да/Нет").lower()
    if user_input_sort == "да":
        ascending_or_descending: str = input("Отсортировать по возрастанию или по убыванию?").lower()
        if ascending_or_descending == "по возрастанию":
            sorted_data: Any = sort_by_date(filtered_by_status, reverse_sort=False)
        elif ascending_or_descending == "по убыванию":
            sorted_data = sort_by_date(filtered_by_status)

    user_input_currency: str = input("Выводить только рублевые транзакции? Да/Нет").lower()
    if user_input_currency == "да":
        currency_trans: Any = sum_from_transaction(sorted_data)
    else:
        currency_trans = sorted_data
    user_input_filter_word: str = input(
        "Отфильтровать список транзакций по определенному слову в описании? Да/Нет"
    ).lower()
    if user_input_filter_word == "да":
        user_word: str = input("Введите слово для фильтрации: ").lower()
        filtered_list_transactions: list[dict] = process_bank_search(currency_trans, user_word)
        results: list[dict] = filtered_list_transactions
    else:
        results = currency_trans

    print("Распечатываю итоговый список транзакций...")
    if results:
        print(f"Всего банковских операций в выборке: {len(results)}")
        pprint(results)
    else:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
