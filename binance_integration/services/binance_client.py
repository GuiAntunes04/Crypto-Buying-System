import time
from binance.client import Client
from decimal import Decimal
from binance.exceptions import BinanceAPIException

class BinanceClientService:
    def __init__(self, api_key: str, secret_key: str):
        self.client = Client(
            api_key=api_key.strip(),
            api_secret=secret_key.strip(),
            testnet=True
        )

        # ✅ sincronização correta de horário
        server_time = self.client.get_server_time()
        local_time = int(time.time() * 1000)

        self.client.timestamp_offset = server_time['serverTime'] - local_time

    def buy_market(self, symbol: str, quantity: float):
        try:
            return self.client.create_order(
                symbol=symbol,
                side=Client.SIDE_BUY,
                type=Client.ORDER_TYPE_MARKET,
                quantity=quantity,
                recvWindow=10000
            )
        except BinanceAPIException as e:
            raise RuntimeError(e.message)
        
    def sell_market(self, symbol: str, quantity: float):
        try:
            return self.client.create_order(
                symbol=symbol,
                side=Client.SIDE_SELL,
                type=Client.ORDER_TYPE_MARKET,
                quantity=quantity,
                recvWindow=10000
            )
        except BinanceAPIException as e:
            raise RuntimeError(e.message)

    
    def get_symbol_info(self, symbol: str):
        return self.client.get_symbol_info(symbol)
    
    def get_price(self, symbol: str):
        price = self.client.get_symbol_ticker(symbol=symbol)
        return Decimal(price['price'])
    
    def get_balance(self, asset: str):
        balance = self.client.get_asset_balance(asset)
        return Decimal(balance['free'])