import datetime as dt
import jwt
import requests

from urllib.parse import urlencode


class LiquidClient:
    def __init__(self, client_id, client_secret):
        self._client_id = client_id
        self._client_secret = client_secret
        self._timestamp = int(dt.datetime.utcnow().timestamp())
        self._uri = "https://api.liquid.com"

    def _auth_payload(self, path):
        payload = {
            'path': path,
            'nonce': self._timestamp,
            'token_id': self._client_id
        }

        encoded_jwt = jwt.encode(payload, self._client_secret, algorithm='HS256')

        return encoded_jwt

    def _request(self, path, is_signed=False):
        signature = self._auth_payload(path) if is_signed else None
        headers = {'X-Quoine-API-Version': '2',
                   'Content-Type': 'application/json',
                   'X-Quoine-Auth': signature}

        url = f'{self._uri}{path}'
        response = requests.get(url, headers=headers)

        if not response.raise_for_status():
            return response.json()
        else:
            response.raise_for_status()

    def get_crypto_accounts(self):
        path = '/crypto_accounts'
        return self._request(path=path, is_signed=True)

    def get_all_account_balances(self):
        path = '/accounts/balance'
        return self._request(path=path, is_signed=True)

    def get_account_details(self, currency: str):
        path = f'/accounts/{currency}'
        return self._request(path=path, is_signed=True)

    def get_trading_accounts(self):
        path = '/trading_accounts'
        return self._request(path=path, is_signed=True)

    def get_product(self, product_id: int):
        path = f'/products/{product_id}'

        return self._request(path=path)

    def get_loans(self, currency: str):
        path = f'/loans?currency={currency}'
        return self._request(path=path, is_signed=True)

    def get_trades(self, **params):
        path = f'/trades?{urlencode(params)}'
        return self._request(path=path, is_signed=True)

    def get_execution(self, product_id: int):
        path = f'/executions/me?product_id={product_id}'
        return self._request(path=path, is_signed=True)
