import pytest
from black.lines import Callable

from src.processing import filter_by_state, sort_by_date


def test_filter_by_state(dict_transaction_data: list) -> None:
    assert filter_by_state(dict_transaction_data) == [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]

    assert filter_by_state(dict_transaction_data, "CANCELED") == [
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


@pytest.mark.parametrize(
    "transaction_data, expected",
    [
        (
            [
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
            [],
        )
    ],
)
def test_filter_by_state_empty_executed(transaction_data: list, expected: list) -> None:
    assert filter_by_state(transaction_data) == expected


@pytest.mark.parametrize(
    "transaction_data_canceled, expected_canceled",
    [
        (
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            ],
            [],
        )
    ],
)
def test_filter_by_state_empty_canceled(transaction_data_canceled: list, expected_canceled: list) -> None:
    assert filter_by_state(transaction_data_canceled, "CANCELED") == expected_canceled


@pytest.mark.parametrize(
    "operation_list, sorted_operation",
    [
        (
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            ],
        )
    ],
)
def test_sort_by_date(operation_list: list, sorted_operation: list) -> None:
    assert sort_by_date(operation_list) == sorted_operation


def test_sort_by_date_reverse(operation_list_default: list, reverse_false_list: list) -> None:
    assert sort_by_date(operation_list_default, False) == reverse_false_list
