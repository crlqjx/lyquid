import datetime as dt
import jwt
import requests
import datetime as dt

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

    def get_products(self):
        path = '/products'
        return self._request(path=path)

    def get_product(self, product_id: int):
        path = f'/products/{product_id}'
        return self._request(path=path)

    def get_perpetual_products(self):
        path = '/products?perpetual=1'
        return self._request(path=path)

    def get_order_book(self, product_id: int, full: bool = True):
        data = {'full': int(full)}
        path = f'/products/{product_id}/price_levels?{urlencode(data)}'
        return self._request(path=path)

    def get_executions(self, product_id: int, limit: int = 20, page: int = 1):
        path = f'/executions?product_id={product_id}&limit={limit}&page={page}'
        return self._request(path=path)

    def get_executions_by_timestamp(self, product_id: int, timestamp: dt.datetime, limit: int = None):
        timestamp = timestamp.timestamp()
        path = f'/executions?product_id={product_id}&timestamp={timestamp}&limit={limit}'
        return self._request(path=path)

    # ************************** Authenticated requests: **************************

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

    def get_trading_account(self, account_id):
        path = f'/trading_accounts/{account_id}'
        return self._request(path=path, is_signed=True)

    def get_loans(self, currency: str):
        path = f'/loans?currency={currency}'
        return self._request(path=path, is_signed=True)

    def get_loan_bids(self, currency: str):
        path = f'/loan_bids?currency={currency}'
        return self._request(path=path, is_signed=True)

    def get_trades(self, **params):
        allowed_params = ['funding_currency', 'product_id', 'status', 'trading_type', 'side']
        for param in params:
            assert param in allowed_params, f'{param} not allowed, must be in {allowed_params}'
        path = f"/trades?{urlencode(params)}"
        return self._request(path=path, is_signed=True)

    def get_lending_transactions(self, currency: str, transaction_type: list = None):
        """
        get lending transactions (unpublished endpoint)
        :param currency: lent currency
        :param transaction_type: 'interest_transfer', 'loan', 'repay', 'loan_fee'
        :return:
        {
            'current_page': 1,
            'models': [
                        {
                            'action_id': None,
                            'created_at': 1584659345,
                            'currency': 'ETH',
                            'exchange_fee': '0.0',
                            'from_account_id': 475492,
                            'from_role': None,
                            'gross_amount': '0.0000035',
                            'id': 400676443,
                            'loan': {'currency': 'ETH', 'quantity': '0.1', 'rate': '0.00007'},
                            'net_amount': '0.0000035',
                            'network_fee': '0.0',
                            'state': 'pending',
                            'to_account_id': 1635604,
                            'to_role': None,
                            'transaction_hash': None,
                            'transaction_type': 'loan_fee'
                        },
                        ...
                     ]
            'total_pages': 10000
        }
        """
        allowed_transaction_types = ['interest_transfer', 'loan', 'repay', 'loan_fee']
        transaction_type = allowed_transaction_types if transaction_type is None else transaction_type
        for transac_type in transaction_type:
            assert transac_type in allowed_transaction_types, f'{transac_type} not valid'
        transaction_type = ','.join(transaction_type)
        path = f"/transactions?currency={currency}&transaction_type={transaction_type}"
        return self._request(path=path, is_signed=True)

    def get_trades_loans(self, trade_id):
        path = f'/trades/{trade_id}/loans'
        return self._request(path=path, is_signed=True)

    def get_orders(self, **params):
        allowed_params = ['funding_currency', 'product_id', 'status', 'trading_type', 'with_details']
        for param in params:
            assert param in allowed_params, f'{param} not allowed, must be in {allowed_params}'
            params[param] = int(params[param]) if isinstance(params[param], bool) else params[param]
        path = f'/orders?{urlencode(params)}'
        return self._request(path=path, is_signed=True)

    def get_my_executions(self, product_id: int):
        path = f'/executions/me?product_id={product_id}'
        return self._request(path=path, is_signed=True)
