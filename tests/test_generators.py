import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


def test_filter_usd(transactions_list: list) -> None:
    result = filter_by_currency(transactions_list, "USD")
    assert len(result) == 3
    for transaction in result:
        assert transaction["operationAmount"]["currency"]["code"] == "USD"


def test_filter_rub(transactions_list: list) -> None:
    result = filter_by_currency(transactions_list, "RUB")
    assert len(result) == 2
    for transaction in result:
        assert transaction["operationAmount"]["currency"]["code"] == "RUB"


def test_filter_wrong_currency(transactions_list: list) -> None:
    assert filter_by_currency(transactions_list, "EUR") == []


def test_filter_empty_list(empty_list: list) -> None:
    assert filter_by_currency(empty_list, "RUB") == []


def test_transaction_descriptions(transactions_list: list, descriptions_result: list) -> None:
    result = list(transaction_descriptions(transactions_list))
    assert len(result) == 5
    assert result == descriptions_result


def test_transaction_descriptions_cut(transactions_list_cut: list) -> None:
    result = list(transaction_descriptions(transactions_list_cut))
    assert len(result) == 2


def test_descriptions_empty_list(empty_list: list) -> None:
    result = list(transaction_descriptions(empty_list))
    assert result == []


def test_card_number_generator(card_gen_result: list) -> None:
    gen = card_number_generator(1, 5)
    assert list(gen) == card_gen_result

    gen = card_number_generator(1, 1)
    assert next(gen) == "0000 0000 0000 0001"

    gen = card_number_generator(1234567890123456, 1234567890123456)
    assert next(gen) == "1234 5678 9012 3456"

    gen = card_number_generator(0, 0)
    assert next(gen) == "0000 0000 0000 0000"

    gen = card_number_generator(9999999999999999, 9999999999999999)
    assert next(gen) == "9999 9999 9999 9999"


def test_card_number_generator_type_errors() -> None:
    with pytest.raises(TypeError) as excinfo:
        list(card_number_generator(1, "3"))
    assert str(excinfo.value) == "Номер карты может содержать только числовые значения"

    with pytest.raises(TypeError) as excinfo:
        list(card_number_generator("1", 3))
    assert str(excinfo.value) == "Номер карты может содержать только числовые значения"

    with pytest.raises(TypeError) as excinfo:
        list(card_number_generator("1", "3"))
    assert str(excinfo.value) == "Номер карты может содержать только числовые значения"

    with pytest.raises(TypeError) as excinfo:
        list(card_number_generator(1.5, 3))
    assert str(excinfo.value) == "Номер карты может содержать только числовые значения"

    with pytest.raises(TypeError) as excinfo:
        list(card_number_generator(1, None))
    assert str(excinfo.value) == "Номер карты может содержать только числовые значения"


def test_card_number_generator_value_errors() -> None:
    with pytest.raises(ValueError) as excinfo:
        list(card_number_generator(3, 1))
    assert str(excinfo.value) == "Начальное значение должно быть меньше конечного"
