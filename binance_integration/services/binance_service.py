# services/binance_service.py
from .binance_client import BinanceClientService
from ..models import BinanceKey, Order
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal
from django.db.models import Sum


class BinanceService:
    def __init__(self, user):
        self.user = user 
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

        if (quantity - min_qty) % step != 0:
            raise ValueError(f"Quantidade deve ser múltiplo de {step}")
        
    def validate_asset_balance(self, symbol: str, quantity: Decimal):
        asset = symbol.replace('USDT', '')
        balance = self.client.get_balance(asset)

        if balance < quantity:
            raise ValueError(
                f"Saldo insuficiente de {asset}. "
                f"Disponível: {balance}, necessário: {quantity}"
            )

    def buy(self, symbol: str, quantity: Decimal):
        if quantity <= 0:
            raise ValueError("Quantidade inválida")

        symbol_info = self.validate_symbol(symbol)

        price = Decimal(str(self.client.get_price(symbol)))
        self.validate_quantity(symbol_info, quantity)
        self.validate_balance(price, quantity)

        response = self.client.buy_market(symbol, float(quantity))

        avg_price = (
            Decimal(response['cummulativeQuoteQty']) /
            Decimal(response['executedQty'])
        )

        order = Order.objects.create(
            user=self.user,
            symbol=symbol,
            side='BUY',
            order_id=response['orderId'],
            price=avg_price,
            quantity=Decimal(response['executedQty']),
            quote_quantity=Decimal(response['cummulativeQuoteQty']),
            status=response['status'],
            raw_response=response
        )

        return order
    
    def sell(self, symbol: str, quantity: Decimal):
        if quantity <= 0:
            raise ValueError("Quantidade inválida")

        symbol_info = self.validate_symbol(symbol)
        self.validate_quantity(symbol_info, quantity)
        self.validate_asset_balance(symbol, quantity)

        response = self.client.sell_market(symbol, float(quantity))

        avg_price = (
            Decimal(response['cummulativeQuoteQty']) /
            Decimal(response['executedQty'])
        )

        order = Order.objects.create(
            user=self.user,
            symbol=symbol,
            side='SELL',
            order_id=response['orderId'],
            price=avg_price,
            quantity=Decimal(response['executedQty']),
            quote_quantity=Decimal(response['cummulativeQuoteQty']),
            status=response['status'],
            raw_response=response
        )

        return order
    
    def get_positions(self):
        positions = []

        symbols = (
            Order.objects
            .filter(user=self.user)
            .values_list('symbol', flat=True)
            .distinct()
        )

        for symbol in symbols:
            buys = Order.objects.filter(
                user=self.user,
                symbol=symbol,
                side='BUY',
                status='FILLED'
            )

            sells = Order.objects.filter(
                user=self.user,
                symbol=symbol,
                side='SELL',
                status='FILLED'
            )

            qty_buy = buys.aggregate(total=Sum('quantity'))['total'] or Decimal('0')
            qty_sell = sells.aggregate(total=Sum('quantity'))['total'] or Decimal('0')

            qty_open = qty_buy - qty_sell
            if qty_open <= 0:
                continue

            cost = buys.aggregate(total=Sum('quote_quantity'))['total']
            avg_price = cost / qty_buy

            current_price = self.client.get_price(symbol)

            pnl_unrealized = (current_price - avg_price) * qty_open

            positions.append({
                'symbol': symbol,
                'quantity': qty_open,
                'avg_price': avg_price,
                'current_price': current_price,
                'pnl_unrealized': pnl_unrealized
            })

        return positions


    
    