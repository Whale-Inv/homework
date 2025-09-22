import os
from unittest.mock import patch, Mock
from requests import Response
from src.external_api import sum_from_transaction


TRANSACTION_RUB = {"operationAmount": {"currency": {"code": "RUB"}, "amount": 100.0}}

TRANSACTION_USD = {"operationAmount": {"currency": {"code": "USD"}, "amount": 1.0}}


MOCK_API_RESPONSE = {"result": 90.0}


def test_sum_rub_transaction():
    result = sum_from_transaction(TRANSACTION_RUB)
    assert result == 100.0


@patch("requests.get")
def test_sum_usd_transaction(mock_get):
    mock_response = Mock(spec=Response)
    mock_response.json.return_value = MOCK_API_RESPONSE
    mock_get.return_value = mock_response

    result = sum_from_transaction(TRANSACTION_USD)
    assert result == 90.0

    mock_get.assert_called_once()
    args, kwargs = mock_get.call_args
    assert kwargs["headers"] == {"apikey": os.getenv("API_KEY")}
    assert kwargs["params"] == {"amount": 1.0, "from": "USD", "to": "RUB"}


@patch("requests.get")
def test_api_error(mock_get):
    mock_get.side_effect = Exception("API error")

    try:
        sum_from_transaction(TRANSACTION_USD)
    except Exception as e:
        assert str(e) == "API error"
    else:
        assert False, "Ожидалось исключение API error"


@patch("requests.get")
def test_invalid_api_response(mock_get):
    mock_response = Mock(spec=Response)
    mock_response.json.return_value = {"error": "Invalid request"}
    mock_get.return_value = mock_response

    try:
        sum_from_transaction(TRANSACTION_USD)
    except Exception as e:
        assert str(e) == "API error"


def test_invalid_transaction_data():
    invalid_transaction = {"operationAmount": {"currency": {"code": "EUR"}, "amount": "не число"}}

    try:
        sum_from_transaction(invalid_transaction)
    except Exception as e:
        assert str(e) == "API error"
