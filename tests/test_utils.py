from unittest.mock import mock_open, patch

import pytest

from src.utils import financial_transaction_data

transaction_list = '[{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]'
empty_file = ''
invalid_json = '{"name": "John"'
not_a_list_data = '{"id": 1, "amount": 100}'

@patch('os.path.exists')
@patch('os.path.getsize')
@patch('builtins.open')
def test_financial_transaction_data_success(mock_open, mock_getsize,mock_exists):
    mock_exists.return_value = True
    mock_getsize.return_value = len(transaction_list)
    mock_open.return_value.__enter__.return_value.read.return_value = transaction_list

    result = financial_transaction_data('test_file.json')
    assert result == [{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]


def test_non_existent_file():
    with patch('os.path.exists', return_value=False):
        result = financial_transaction_data('non_existent_file.json')
        assert result == []


def test_empty_file():
    with patch('os.path.exists', return_value=True):
        with patch('os.path.getsize', return_value=0):
            result = financial_transaction_data('empty_file.json')
            assert result == []


def test_invalid_json():
    with patch('os.path.exists', return_value=True):
        with patch('os.path.getsize', return_value=len(transaction_list)):
            with patch('builtins.open', mock_open(read_data=invalid_json)):
                result = financial_transaction_data('invalid_json_file.json')
                assert result == "Файл содержит невалидный JSON"


def test_type_error():
    with patch('os.path.exists', return_value=True):
        with patch('os.path.getsize', return_value=len(not_a_list_data)):
            with patch('builtins.open', mock_open(read_data=not_a_list_data)):
                result = financial_transaction_data('not_list_file.json')
                assert result == []


def test_not_list_data():
    not_list_data = '{"key": "value"}'
    with patch('builtins.open', mock_open(read_data=not_list_data)):
        result = financial_transaction_data('not_list_file.json')
        assert result == []
