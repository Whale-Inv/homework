def filter_by_state(user_date: list, state: str = "EXECUTED") -> list:
    """Функция, которая принимает список словарей на входе и опционально
    значение для выборки. По умолчанию задано EXECUTED. На выходе
    возвращает выборку словарей в виде списка
    """
    new_user_date = []

    for elem in user_date:
        if elem.get("state") == state:
            new_user_date.append(elem)
    return new_user_date


def sort_by_date(user_date: list, reverse_sort: bool = True) -> list:
    # Используем get_date напрямую в sorted()
    sorted_data = sorted(user_date, key=lambda x: x["date"], reverse=reverse_sort)
    return sorted_data
