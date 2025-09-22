import os

import requests
from dotenv import load_dotenv
from requests import Response

load_dotenv()

API_KEY: str | None = os.getenv("API_KEY")


def sum_from_transaction(my_transaction: dict) -> float:
    """
    функцию, которая принимает на вход транзакцию и возвращает сумму транзакции (amount) в рублях,
    тип данных — float. Если транзакция была в валюте, то
    происходит обращение к внешнему API для получения текущего курса валют и конвертации суммы операции в рубли.
    """
    try:
        if my_transaction["operationAmount"]["currency"]["code"] == "RUB":
            data_amount: float = my_transaction["operationAmount"]["amount"]
        else:
            url: str = "https://api.apilayer.com/exchangerates_data/convert"
            payload: dict = {
                "amount": my_transaction["operationAmount"]["amount"],
                "from": my_transaction["operationAmount"]["currency"]["code"],
                "to": "RUB",
            }
            headers: dict = {"apikey": API_KEY}

            try:
                response: Response = requests.get(url, headers=headers, params=payload)
                print(response.json())
                result: dict = response.json()

                if "result" in result:
                    data_amount = result["result"]
                else:
                    raise KeyError("Ключ 'result' отсутствует в ответе API")

            except Exception as e:
                print(f"Непредвиденная ошибка: {str(e)}")
                raise Exception("API error") from e

    except (KeyError, TypeError) as e:

        print(f"Ошибка в данных транзакции: {str(e)}")
        raise Exception("Invalid transaction data") from e

    return data_amount
