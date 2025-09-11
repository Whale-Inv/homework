import os

from src.decorators import log


def test_log_decorator_success(capsys):
    @log()
    def add_numbers(a, b):
        return a + b

    add_numbers(3, 5)
    captured = capsys.readouterr()
    assert captured.out == "add_numbers ok\n\n"


def test_log_decorator_denied(capsys):
    @log()
    def add_numbers(a, b):
        return a + b

    add_numbers("3", 5)
    captured = capsys.readouterr()
    assert captured.out == "add_numbers error: TypeError. Inputs: '3', 5\n"


def test_writing_file():
    test_file_path = "tests/qwer.txt"

    @log(test_file_path)
    def add_numbers(a, b):
        return a + b


    add_numbers(3, 5)

    # Проверяем существование файла
    assert os.path.exists(test_file_path)

    # Проверяем содержимое
    with open(test_file_path, 'r') as file:
        content = file.read().strip()
        assert content == "add_numbers ok", f"Неверное содержимое файла: {content}"

    os.remove(test_file_path)


def test_writing_file_wrong():
    test_file_path = "tests/qwer.txt"

    @log(test_file_path)
    def add_numbers(a, b):
        return a + b


    add_numbers("3", 5)

    # Проверяем существование файла
    assert os.path.exists(test_file_path)

    # Проверяем содержимое
    with open(test_file_path, 'r') as file:
        content = file.read().strip()
        assert content == "add_numbers error: TypeError. Inputs: '3', 5", f"Неверное содержимое файла: {content}"

    os.remove(test_file_path)