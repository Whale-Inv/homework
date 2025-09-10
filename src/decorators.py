from functools import wraps
from typing import Any, Callable


def log(filename: str | None = None) -> Callable:
    """
log - декоратор с параметрами. Предназначен для автоматической регистрации деталей выполнения функций,
такие как время вызова, имя функции, передаваемые аргументы, результат выполнения и информация об ошибках.
Это позволит обеспечить более глубокий контроль и анализ поведения программы в процессе ее выполнения.
    """
    def wrapper(function: Callable) -> Callable:
        @wraps(function)
        def inner(*args: tuple[Any], **kwargs: dict[str, Any]) -> Any:
            try:
                result: Any = function(*args, **kwargs)
                error_info: Any = None
            except Exception as e:
                args_repr = [repr(a) for a in args]
                kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
                all_args = ", ".join(args_repr + kwargs_repr)

                error_info = {"type": f"{type(e).__name__}", "input": f"{all_args}"}
                result = None

            log_message: Any = f"{function.__name__} "
            if error_info:
                log_message += f"error: {error_info['type']}. "
                log_message += f"Inputs: {error_info['input']}"
            else:
                log_message += "ok\n"

            if filename:
                with open(filename, "a") as f:
                    f.write(log_message)
            else:
                print(log_message)

            return result

        return inner

    return wrapper
