# services/binance_service.py
from .binance_client import BinanceClientService
from ..models import BinanceKey
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal


class BinanceService:
    def __init__(self, user):
        try:
            keys = BinanceKey.objects.get(user=user)
        except ObjectDoesNotExist:
            raise ValueError("Usuário não possui chaves da Binance cadastradas")

        self.client = BinanceClientService(
            api_key=keys.api_key,
            secret_key=keys.get_secret_key()
        )

    def validate_symbol(self, symbol: str):
        info = self.client.get_symbol_info(symbol)
        if info is None:
            raise ValueError("Símbolo inválido ou inexistente na Binance")
        return info

    def validate_balance(self, price: float, quantity: float):
        required = price * quantity
        balance = self.client.get_balance('USDT')

        if balance < required:
            raise ValueError(
                f"Saldo insuficiente. Necessário: {required:.2f} USDT, disponível: {balance:.2f}"
            )
        
    def validate_quantity(self, symbol_info, quantity: Decimal):
        lot = next(
            f for f in symbol_info['filters']
            if f['filterType'] == 'LOT_SIZE'
        )

        min_qty = Decimal(lot['minQty'])
        step = Decimal(lot['stepSize'])

        if quantity < min_qty:
            raise ValueError(f"Quantidade mínima: {min_qty}")

        # evita erro de precisão
        remainder = (quantity - min_qty) % step

        if remainder != 0:
            raise ValueError(f"Quantidade deve ser múltiplo de {step}")

    
    def buy(self, symbol: str, quantity):
        if quantity <= 0:
            raise ValueError("Quantidade inválida")

        symbol_info = self.validate_symbol(symbol)
        price = self.client.get_price(symbol)  # já retorna Decimal
        self.validate_quantity(symbol_info, quantity)
        self.validate_balance(price, quantity)

        return self.client.buy_market(symbol, float(quantity))
    