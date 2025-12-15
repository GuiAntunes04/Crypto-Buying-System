# services/binance_service.py
from .binance_client import BinanceClientService
from ..models import BinanceKey


class BinanceService:
    def __init__(self, user):
        keys = BinanceKey.objects.get(user=user)

        self.client = BinanceClientService(
            api_key=keys.api_key,
            secret_key=keys.get_secret_key()
        )

    def buy(self, symbol: str, quantity: float):
        if quantity <= 0:
            raise ValueError("Quantidade inválida")

        return self.client.buy_market(symbol, quantity)
