from binance.client import Client

class BinanceService:
    def __init__(self, api_key: str, secret_key: str, testnet=True):
        self.client = Client(api_key, secret_key)

        if testnet:
            self.client.API_URL = 'https://testnet.binance.vision/api'

    def get_price(self, symbol: str):
        return self.client.get_symbol_ticker(symbol=symbol)
