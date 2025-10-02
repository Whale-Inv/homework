from unittest.mock import mock_open, patch

import pandas as pd

from src.csv_excel_reader import csv_reader, excel_reader

MOCK_DATA = pd.DataFrame({"id": [1, 2, 3], "name": ["Иван", "Петр", "Анна"], "amount": [100, 200, 300]})

EXPECTED_PD_RESULT = [
    {"id": 1, "name": "Иван", "amount": 100},
    {"id": 2, "name": "Петр", "amount": 200},
    {"id": 3, "name": "Анна", "amount": 300},
]

CSV_CONTENT = """id,name,amount
1,Иван,100
2,Петр,200
3,Анна,300"""

EXPECTED_RESULT = [
    {"id": "1", "name": "Иван", "amount": "100"},
    {"id": "2", "name": "Петр", "amount": "200"},
    {"id": "3", "name": "Анна", "amount": "300"},
]


def test_csv_reader_file_not_found():
    with patch("os.path.exists", return_value=False):
        result = csv_reader("file_not_found.csv")
        assert result == "Файл не найден"


def test_csv_reader_not_csv():
    result = csv_reader("../data/operations.json")
    assert result == "Расширение файла не CSV"


@patch("os.path.exists", return_value=True)
@patch("builtins.open", new_callable=mock_open, read_data=CSV_CONTENT)
def test_csv_reader_success(mock_open, mock_exists):
    result = csv_reader("test.csv")
    assert result == EXPECTED_RESULT

    mock_exists.assert_called_once_with("test.csv")
    mock_open.assert_called_once_with("test.csv", "r", encoding="utf-8")


def test_excel_reader_file_not_found():
    with patch("os.path.exists", return_value=False):
        result = excel_reader("file_not_found.xlsx")
        assert result == "Файл не найден"


def test_excel_reader_not_xlsx():
    result = excel_reader("../data/operations.json")
    assert result == "Расширение файла не xlsx"


@patch("os.path.exists", return_value=True)
@patch("pandas.read_excel")
def test_excel_reader_success(mock_read_excel, mock_exists):
    mock_read_excel.return_value = MOCK_DATA

    result = excel_reader("test.xlsx")

    assert result == EXPECTED_PD_RESULT

    mock_exists.assert_called_once_with("test.xlsx")
    mock_read_excel.assert_called_once_with("test.xlsx")
