import unittest
from unittest.mock import mock_open, patch

from src.utils import financial_transaction_data, process_bank_operations, process_bank_search

transaction_list = '[{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]'
empty_file = ""
invalid_json = '{"name": "John"'
not_a_list_data = '{"id": 1, "amount": 100}'


@patch("os.path.exists")
@patch("os.path.getsize")
@patch("builtins.open")
def test_financial_transaction_data_success(mock_open, mock_getsize, mock_exists):
    mock_exists.return_value = True
    mock_getsize.return_value = len(transaction_list)
    mock_open.return_value.__enter__.return_value.read.return_value = transaction_list

    result = financial_transaction_data("test_file.json")
    assert result == [{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]


def test_non_existent_file():
    with patch("os.path.exists", return_value=False):
        result = financial_transaction_data("non_existent_file.json")
        assert result == []


def test_empty_file():
    with patch("os.path.exists", return_value=True):
        with patch("os.path.getsize", return_value=0):
            result = financial_transaction_data("empty_file.json")
            assert result == []


def test_invalid_json():
    with patch("os.path.exists", return_value=True):
        with patch("os.path.getsize", return_value=len(transaction_list)):
            with patch("builtins.open", mock_open(read_data=invalid_json)):
                result = financial_transaction_data("invalid_json_file.json")
                assert result == "Файл содержит невалидный JSON"


def test_type_error():
    with patch("os.path.exists", return_value=True):
        with patch("os.path.getsize", return_value=len(not_a_list_data)):
            with patch("builtins.open", mock_open(read_data=not_a_list_data)):
                result = financial_transaction_data("not_list_file.json")
                assert result == []


def test_not_list_data():
    not_list_data = '{"key": "value"}'
    with patch("builtins.open", mock_open(read_data=not_list_data)):
        result = financial_transaction_data("not_list_file.json")
        assert result == []


class TestBankSearch(unittest.TestCase):

    def setUp(self):
        # Создаем тестовые данные
        self.test_data = [
            {"id": 1, "description": "Покупка в магазине продуктов", "amount": 1000},
            {"id": 2, "description": "Оплата коммунальных услуг", "amount": 5000},
            {"id": 3, "description": "Перевод другу", "amount": 2000},
            {"id": 4, "description": "Покупка продуктов в супермаркете", "amount": 1500},
        ]

    def test_normal_search(self):
        # Базовый тест поиска
        result = process_bank_search(self.test_data, "продуктов")
        self.assertEqual(len(result), 2)
        for item in result:
            self.assertIn("продуктов", item["description"])

    def test_empty_search(self):
        # Поиск пустой строки
        result = process_bank_search(self.test_data, "")
        self.assertEqual(len(result), len(self.test_data))

    def test_no_matches(self):
        # Поиск несуществующего значения
        result = process_bank_search(self.test_data, "несуществующее")
        self.assertEqual(len(result), 0)

    def test_mixed_data_types(self):
        # Данные с разными типами значений
        mixed_data = [
            {"description": "текст", "amount": 100},
            {"description": 12345, "amount": 200},  # нестроковое значение
            {"description": "еще текст"},
        ]
        result = process_bank_search(mixed_data, "текст")
        self.assertEqual(len(result), 2)

    def test_empty_data(self):
        # Пустой список данных
        result = process_bank_search([], "поиск")
        self.assertEqual(result, [])

    def test_non_string_values(self):
        # Значения, которые не являются строками
        data = [
            {"description": None},
            {"description": 123},
            {"description": True},
            {"description": {"nested": "dict"}},
        ]
        result = process_bank_search(data, "поиск")
        self.assertEqual(result, [])


class TestBankOperations(unittest.TestCase):
    def setUp(self):
        # Создаем тестовые данные
        self.test_data = [
            {"description": "Продукты", "amount": 1000},
            {"description": "Транспорт", "amount": 500},
            {"description": "Продукты", "amount": 700},
            {"description": "Развлечения", "amount": 1500},
            {"description": "Транспорт", "amount": 300},
        ]
        self.test_categories = ["Продукты", "Транспорт", "Развлечения", "Коммунальные"]

    def test_normal_processing(self):
        # Базовый тест подсчета операций
        result = process_bank_operations(self.test_data, self.test_categories)
        expected = {"Продукты": 2, "Транспорт": 2, "Развлечения": 1, "Коммунальные": 0}
        self.assertEqual(result, expected)

    def test_empty_data(self):
        # Тест с пустым списком операций
        result = process_bank_operations([], self.test_categories)
        expected = {"Продукты": 0, "Транспорт": 0, "Развлечения": 0, "Коммунальные": 0}
        self.assertEqual(result, expected)

    def test_no_matching_categories(self):
        # Тест с категориями, которых нет в данных
        result = process_bank_operations(self.test_data, ["Другое", "Новое"])
        expected = {"Другое": 0, "Новое": 0}
        self.assertEqual(result, expected)

    def test_missing_description(self):
        # Тест с отсутствующим описанием
        data = [{"amount": 1000}, {"description": "Продукты", "amount": 700}]
        result = process_bank_operations(data, self.test_categories)
        expected = {"Продукты": 1, "Транспорт": 0, "Развлечения": 0, "Коммунальные": 0}
        self.assertEqual(result, expected)

    def test_non_string_description(self):
        # Тест с нестроковым описанием
        data = [{"description": 123}, {"description": "Продукты"}, {"description": True}]
        result = process_bank_operations(data, self.test_categories)
        expected = {"Продукты": 1, "Транспорт": 0, "Развлечения": 0, "Коммунальные": 0}
        self.assertEqual(result, expected)

    def test_mixed_data(self):
        # Тест со смешанными данными
        data = [
            {"description": "Продукты"},
            {"description": "Транспорт"},
            {"description": "Продукты"},
            {"description": "Развлечения"},
            {"description": "Неизвестная категория"},
        ]
        result = process_bank_operations(data, self.test_categories)
        expected = {"Продукты": 2, "Транспорт": 1, "Развлечения": 1, "Коммунальные": 0}
        self.assertEqual(result, expected)

    def test_large_data(self):
        # Тест с большим объемом данных
        large_data = self.test_data * 1000
        result = process_bank_operations(large_data, self.test_categories)
        expected = {"Продукты": 2000, "Транспорт": 2000, "Развлечения": 1000, "Коммунальные": 0}
        self.assertEqual(result, expected)

    def test_empty_categories(self):
        # Тест с пустым списком категорий
        result = process_bank_operations(self.test_data, [])
        self.assertEqual(result, {})

    def test_invalid_operation_type(self):
        # Тест с некорректным типом операции
        invalid_data = [{"description": "Продукты"}, "не_словарь", {"description": "Транспорт"}]
        result = process_bank_operations(invalid_data, self.test_categories)
        expected = {"Продукты": 1, "Транспорт": 1, "Развлечения": 0, "Коммунальные": 0}
        self.assertEqual(result, expected)

    def test_all_categories_present(self):
        # Тест когда все категории присутствуют в данных
        data = [
            {"description": "Продукты"},
            {"description": "Транспорт"},
            {"description": "Развлечения"},
            {"description": "Коммунальные"},
        ]
        result = process_bank_operations(data, self.test_categories)
        expected = {"Продукты": 1, "Транспорт": 1, "Развлечения": 1, "Коммунальные": 1}
        self.assertEqual(result, expected)

    def test_multiple_same_categories(self):
        # Тест с множественными одинаковыми категориями
        data = [
            {"description": "Продукты"},
            {"description": "Продукты"},
            {"description": "Продукты"},
            {"description": "Транспорт"},
        ]
        result = process_bank_operations(data, self.test_categories)
        expected = {"Продукты": 3, "Транспорт": 1, "Развлечения": 0, "Коммунальные": 0}
        self.assertEqual(result, expected)

    def test_whitespace_in_description(self):
        # Тест с пробелами в описании
        data = [{"description": " Продукты "}, {"description": " Транспорт"}, {"description": "Развлечения "}]
        categories = ["Продукты", "Транспорт", "Развлечения"]
        result = process_bank_operations(data, categories)
        expected = {"Продукты": 0, "Транспорт": 0, "Развлечения": 0}
        self.assertEqual(result, expected)

        # Проверяем с учетом пробелов в категориях
        categories_with_spaces = [" Продукты ", " Транспорт", "Развлечения "]
        result = process_bank_operations(data, categories_with_spaces)
        expected = {" Продукты ": 1, " Транспорт": 1, "Развлечения ": 1}
        self.assertEqual(result, expected)
