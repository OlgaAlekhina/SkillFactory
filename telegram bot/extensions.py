import requests
import json
from config import keys, my_api_key

class APIException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        if quote == base:
            raise APIException('Валюты должны быть разными.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Приложение не работает с валютой {quote}.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Приложение не работает с валютой {base}.')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException('Некорректно введено количество валюты.')

        r = requests.get(
            f'https://api.fastforex.io/convert?from={base_ticker}&to={quote_ticker}&amount={amount}&api_key={my_api_key}')
        text = json.loads(r.content)
        total_amount = text['result'][keys[quote]]

        return total_amount