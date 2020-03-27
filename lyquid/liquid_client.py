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
        """
        Get the list of all available products
        :return:
        [
            {
                "id": 5,
                "product_type": "CurrencyPair",
                "code": "CASH",
                "name": "CASH Trading",
                "market_ask": "48203.05",
                "market_bid": "48188.15",
                "indicator": -1,
                "currency": "JPY",
                "currency_pair_code": "BTCJPY",
                "symbol": "¥",
                "fiat_minimum_withdraw": "1500.0",
                "pusher_channel": "product_cash_btcjpy_5",
                "taker_fee": "0.0",
                "maker_fee": "0.0",
                "low_market_bid": "47630.99",
                "high_market_ask": "48396.71",
                "volume_24h": "2915.627366519999999998",
                "last_price_24h": "48217.2",
                "last_traded_price": "48203.05",
                "last_traded_quantity": "1.0",
                "quoted_currency": "JPY",
                "base_currency": "BTC",
                "exchange_rate": "0.009398151671149725",
                "timestamp": "1576739219.195353100"
            },
            ...
        ]
        """
        path = '/products'
        return self._request(path=path)

    def get_product(self, product_id: int):
        """
        Get a product from its id
        :param product_id: integer
        :return:
        {
            "id": 5,
            "product_type": "CurrencyPair",
            "code": "CASH",
            "name": "CASH Trading",
            "market_ask": "48203.05",
            "market_bid": "48188.15",
            "indicator": -1,
            "currency": "JPY",
            "currency_pair_code": "BTCJPY",
            "symbol": "¥",
            "fiat_minimum_withdraw": "1500.0",
            "pusher_channel": "product_cash_btcjpy_5",
            "taker_fee": "0.0",
            "maker_fee": "0.0",
            "low_market_bid": "47630.99",
            "high_market_ask": "48396.71",
            "volume_24h": "2915.62736652",
            "last_price_24h": "48217.2",
            "last_traded_price": "48203.05",
            "last_traded_quantity": "1.0",
            "quoted_currency": "JPY",
            "base_currency": "BTC",
            "exchange_rate": "0.009398151671149725",
            "timestamp": "1576739219.195353100"
        }
        """
        path = f'/products/{product_id}'
        return self._request(path=path)

    def get_perpetual_products(self):
        """
        Get the list of all available perpetual products
        :return:
        [
            {
                "id": "603",
                "product_type": "Perpetual",
                "code": "CASH",
                "name": null,
                "market_ask": "1143900",
                "market_bid": "1143250",
                "currency": "JPY",
                "currency_pair_code": "P-BTCJPY",
                "pusher_channel": "product_cash_p-btcjpy_603",
                "taker_fee": "0.0",
                "maker_fee": "0.0",
                "low_market_bid": "1124450.0",
                "high_market_ask": "1151750.0",
                "volume_24h": "0.1756",
                "last_price_24h": "1129850.0",
                "last_traded_price": "1144700.0",
                "last_traded_quantity": "0.014",
                "quoted_currency": "JPY",
                "base_currency": "P-BTC",
                "tick_size": "50.0",
                "perpetual_enabled": true,
                "index_price": "1142636.03935",
                "mark_price": "1143522.18417",
                "funding_rate": "0.00033",
                "fair_price": "1143609.31009",
                "timestamp": "1581558659.195353100",
            },
            ...
        ]
        """
        path = '/products?perpetual=1'
        return self._request(path=path)

    def get_order_book(self, product_id: int, full: int = 1):
        """
        Get order book
        :param product_id: integer
        :param full: integer - 1 to get all price levels (default is 20 each side)
        :return:
        {
          "buy_price_levels": [
            ["416.23000", "1.75000"],   ...
          ],
          "sell_price_levels": [
            ["416.47000", "0.28675"],   ...
          ],
          "timestamp": "1576729943.772247300"
        }
        """
        data = {'full': int(full)}
        path = f'/products/{product_id}/price_levels?{urlencode(data)}'
        return self._request(path=path)

    def get_executions(self, product_id: int, limit: int = 20, page: int = 1):
        """
        Get a list of recent executions from a product (Executions are sorted in DESCENDING order - Latest first)
        :param product_id: integer
        :param limit: integer - How many executions should be returned. Must be <= 1000. Default is 20
        :param page: integer - From what page the executions should be returned, e.g if limit=20 and page=2, the
        response would start from the 21st execution. Default is 1
        :return:
        {
          "models": [
            {
              "id": 1011880,
              "quantity": "6.118954",
              "price": "409.78",
              "taker_side": "sell",
              "created_at": 1457370745
            },
            {
              "id": 1011791,
              "quantity": "1.15",
              "price": "409.12",
              "taker_side": "sell",
              "created_at": 1457365585
            }
          ],
          "current_page": 2,
          "total_pages": 1686
        }
        """
        path = f'/executions?product_id={product_id}&limit={limit}&page={page}'
        return self._request(path=path)

    def get_executions_by_timestamp(self, product_id: int, timestamp: dt.datetime, limit: int = None):
        """
        Get a list of executions after a particular time (Executions are sorted in ASCENDING order)
        :param product_id: integer
        :param timestamp: datetime
        :param limit: integer - How many executions should be returned. Must be <= 1000. Default is 20
        :return:
        """
        timestamp = timestamp.timestamp()
        path = f'/executions?product_id={product_id}&timestamp={timestamp}&limit={limit}'
        return self._request(path=path)

    # ************************** Authenticated requests: **************************

    def get_crypto_accounts(self):
        """
        :return:
        [
          {
            "id": 4668,
            "balance": "4.99",
            "reserved_balance": "0.0",
            "address": "1F25zWAQ1BAAmppNxLV3KtK6aTNhxNg5Hg",
            "currency": "BTC",
            "currency_symbol": "฿",
            "pusher_channel": "user_3020_account_btc",
            "minimum_withdraw": 0.02,
            "lowest_offer_interest_rate": "0.00049",
            "highest_offer_interest_rate": "0.05000",
            "currency_type": "crypto"
          }
        ]
        """
        path = '/crypto_accounts'
        return self._request(path=path, is_signed=True)

    def get_all_account_balances(self):
        """
        :return:
        [
            {
                "currency": "BTC",
                "balance": "0.04925688"
            },
            {
                "currency": "USD",
                "balance": "7.17696"
            },
            {
                "currency": "JPY",
                "balance": "356.01377"
            }
        ]
        """
        path = '/accounts/balance'
        return self._request(path=path, is_signed=True)

    def get_account_details(self, currency: str):
        """
        :param currency: string
        :return:
        [
          {"object_type": "Order", "object_id": 1, "amount": "4004.0"},
          {"object_type": "LoanBid", "object_id": 2, "amount": "1000.0"},
          {"object_type": "Trade", "object_id": 3, "amount": "200.0"},
          {"object_type": "Trade", "object_id": 4, "amount": "800.0"}
        ]
        """
        path = f'/accounts/{currency}'
        return self._request(path=path, is_signed=True)

    def get_trading_accounts(self):
        """
        :return:
        [
          {
            "id": 1759,
            "leverage_level": 10,
            "max_leverage_level": 10,
            "pnl": "0.0",
            "equity": "10000.1773",
            "margin": "4.2302",
            "free_margin": "9995.9471",
            "trader_id": 4807,
            "status": "active",
            "product_code": "CASH",
            "currency_pair_code": "BTCUSD",
            "position": "0.1",
            "balance": "10000.1773",
            "created_at": 1421992165,
            "updated_at": 1457242996,
            "pusher_channel": "trading_account_1759",
            "margin_percent": "0.1",
            "product_id": 1,
            "funding_currency": "USD"
          },
        ...
        ]
        """
        path = '/trading_accounts'
        return self._request(path=path, is_signed=True)

    def get_trading_account(self, account_id):
        """
        Get a trading account from its id
        :param account_id: integer
        :return:
        {
          "id": 1759,
          "leverage_level": 10,
          "max_leverage_level": 10,
          "pnl": "0.0",
          "equity": "10000.1773",
          "margin": "4.2302",
          "free_margin": "9995.9471",
          "trader_id": 4807,
          "status": "active",
          "product_code": "CASH",
          "currency_pair_code": "BTCUSD",
          "position": "0.1",
          "balance": "10000.1773",
          "created_at": 1421992165,
          "updated_at": 1457242996,
          "pusher_channel": "trading_account_1759",
          "margin_percent": "0.1",
          "product_id": 1,
          "funding_currency": "USD"
        }
        """
        path = f'/trading_accounts/{account_id}'
        return self._request(path=path, is_signed=True)

    def get_loans(self, currency: str):
        """
        Get loans from a currency
        :param currency: string
        :return:
        {
          "models": [
            {
              "id": 144825,
              "quantity": "495.1048",
              "rate": "0.0005",
              "created_at": 1464168246,
              "lender_id": 312,
              "borrower_id": 5712,
              "status": "open",
              "currency": "JPY",
              "fund_reloaned": true
            }
          ],
          "current_page": 1,
          "total_pages": 1
        }
        """
        path = f'/loans?currency={currency}'
        return self._request(path=path, is_signed=True)

    def get_loan_bids(self, currency: str):
        """
        get loans bid from currency
        :param currency: string
        :return:
        {
          "models": [
            {
              "id": 3580,
              "bidask_type": "limit",
              "quantity": "50.0",
              "currency": "USD",
              "side": "bid",
              "filled_quantity": "0.0",
              "status": "live",
              "rate": "0.0007",
              "user_id": 3020
            }
          ],
          "current_page": 1,
          "total_pages": 1
        }
        """
        path = f'/loan_bids?currency={currency}'
        return self._request(path=path, is_signed=True)

    def get_trades(self, **params):
        """
        :param params: 'funding_currency', 'product_id', 'status', 'trading_type' or 'side'
        :return:
        {
          "models": [
            {
              "id": 57896,
              "currency_pair_code": "BTCUSD",
              "status": "open",
              "side": "short",
              "margin_type": "cross",
              "margin_used": "0.83588",
              "liquidation_price": null,
              "maintenance_margin": null,
              "open_quantity": "0.01",
              "close_quantity": "0.0",
              "quantity": "0.01",
              "leverage_level": 5,
              "product_code": "CASH",
              "product_id": 1,
              "open_price": "417.65",
              "close_price": "417.0",
              "trader_id": 3020,
              "open_pnl": "0.0",
              "close_pnl": "0.0",
              "pnl": "0.0065",
              "stop_loss": "0.0",
              "take_profit": "0.0",
              "funding_currency": "USD",
              "created_at": 1456250726,
              "updated_at": 1456251837,
              "total_interest": "0.02"
            },
            ...
          ],
          "current_page": 1,
          "total_pages": 1
        }
        """
        allowed_params = ['funding_currency', 'product_id', 'status', 'trading_type', 'side']
        for param in params:
            assert param in allowed_params, f'{param} not allowed, must be in {allowed_params}'
        path = f"/trades?{urlencode(params)}"
        return self._request(path=path, is_signed=True)

    def get_lending_transactions(self, currency: str, transaction_type: list = None, page: int = 1, limit: int = 20):
        """
        get lending transactions (unpublished endpoint)
        :param currency: lent currency
        :param transaction_type: 'interest_transfer', 'loan', 'repay', 'loan_fee'
        :param page: From what page the transactions should be returned, e.g if limit=20 and page=2, the response would
        start from the 21st transaction. Default is 1
        :param limit: How many transactions should be returned. Must be <= 1000. Default is 20
        :return: list of lending transactions from a currency (Executions are sorted in DESCENDING order - Latest first)
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
        path = f"/transactions?currency={currency}&transaction_type={transaction_type}&page={page}&limit={limit}"
        return self._request(path=path, is_signed=True)

    def get_trades_loans(self, trade_id):
        """
        Get trades loans from trade id
        :param trade_id: integer
        :return:
        [
          {
            "id": 103520,
            "quantity": "42.302",
            "rate": "0.0002",
            "created_at": 1461998432,
            "lender_id": 100,
            "borrower_id": 3020,
            "status": "open",
            "currency": "USD",
            "fund_reloaned": true
          }
        ]
        """
        path = f'/trades/{trade_id}/loans'
        return self._request(path=path, is_signed=True)

    def get_orders(self, **params):
        """

        :param params: 'funding_currency', 'product_id', 'status', 'trading_type' or 'with_details'
        :return:
        {
          "models": [
            {
              "id": 2157474,
              "order_type": "limit",
              "margin_type": null,
              "quantity": "0.01",
              "disc_quantity": "0.0",
              "iceberg_total_quantity": "0.0",
              "side": "sell",
              "filled_quantity": "0.0",
              "price": "500.0",
              "created_at": 1462123639,
              "updated_at": 1462123639,
              "status": "live",
              "leverage_level": 1,
              "source_exchange": "QUOINE",
              "product_id": 1,
              "product_code": "CASH",
              "funding_currency": "USD",
              "currency_pair_code": "BTCUSD",
              "order_fee": "0.0",
              *
              "executions": []
              *
            }
          ],
          "current_page": 1,
          "total_pages": 1
        }
        """
        allowed_params = ['funding_currency', 'product_id', 'status', 'trading_type', 'with_details']
        for param in params:
            assert param in allowed_params, f'{param} not allowed, must be in {allowed_params}'
            params[param] = int(params[param]) if isinstance(params[param], bool) else params[param]
        path = f'/orders?{urlencode(params)}'
        return self._request(path=path, is_signed=True)

    def get_my_executions(self, product_id: int):
        """
        :param product_id:
        :return:
        {
          "models": [
            {
              "id": 1001232,
              "quantity": "0.37153179",
              "price": "390.0",
              "taker_side": "sell",
              "my_side": "sell",
              "created_at": 1457193798,
              "order_id": 2157474,
              "client_order_id": "e77b5a4f-649d-422a-aca3-e02c40a65f55"
            }
          ],
          "current_page": 1,
          "total_pages": 2
        }
        """
        path = f'/executions/me?product_id={product_id}'
        return self._request(path=path, is_signed=True)
