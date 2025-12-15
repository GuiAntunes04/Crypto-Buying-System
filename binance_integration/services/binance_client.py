import time
from binance.client import Client


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
        return self.client.create_order(
            symbol=symbol,
            side=Client.SIDE_BUY,
            type=Client.ORDER_TYPE_MARKET,
            quantity=quantity,
            recvWindow=10000
        )
