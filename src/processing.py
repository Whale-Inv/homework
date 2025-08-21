def filter_by_state(transaction_data: list[dict], state: str = "EXECUTED") -> list[dict]:
    """Функция, которая принимает список словарей на входе и опционально
    значение для выборки. По умолчанию задано EXECUTED. На выходе
    возвращает выборку словарей в виде списка
    """
    new_transaction_data: list = []

    for elem in transaction_data:
        if elem.get("state") == state:
            new_transaction_data.append(elem)
    return new_transaction_data


def sort_by_date(operation_list: list[dict], reverse_sort: bool = True) -> list[dict]:
    """Функция, которая сортирует список словарей по дате. По умолчанию,
    сортировка выполняется по убыванию.
    """
    sorted_data = sorted(operation_list, key=lambda x: x["date"], reverse=reverse_sort)
    return sorted_data
