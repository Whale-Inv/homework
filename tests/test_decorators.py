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
