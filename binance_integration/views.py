from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView
from .serializers import OrderSerializer, OrderResponseSerializer
from .services.binance_service import BinanceService
from .models import BinanceKey, Order


# 🔹 VIEW PARA SALVAR AS CHAVES DA BINANCE
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_binance_keys(request):
    api_key = request.data.get('api_key')
    secret_key = request.data.get('secret_key')

    if not api_key or not secret_key:
        return Response(
            {"error": "api_key and secret_key are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    keys, _ = BinanceKey.objects.get_or_create(user=request.user)
    keys.api_key = api_key
    keys.set_secret_key(secret_key)
    keys.save()

    return Response(
        {"message": "Binance keys saved successfully"},
        status=status.HTTP_201_CREATED
    )

class MarketBuyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = BinanceService(request.user)

        try:
            order = service.buy(
                symbol=serializer.validated_data['symbol'],
                quantity=serializer.validated_data['quantity']
            )

        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        except RuntimeError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_502_BAD_GATEWAY
            )
        response_serializer = OrderResponseSerializer(order)

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )
    
class MarketSellView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = BinanceService(request.user)

        try:
            order = service.sell(
                symbol=serializer.validated_data['symbol'],
                quantity=serializer.validated_data['quantity']
            )

        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        except RuntimeError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_502_BAD_GATEWAY
            )

        return Response(
            OrderResponseSerializer(order).data,
            status=status.HTTP_201_CREATED
        )
    
class OrderListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderResponseSerializer

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user)

        symbol = self.request.query_params.get('symbol')
        side = self.request.query_params.get('side')
        status = self.request.query_params.get('status')

        if symbol:
            queryset = queryset.filter(symbol=symbol)

        if side:
            queryset = queryset.filter(side=side)

        if status:
            queryset = queryset.filter(status=status)

        return queryset.order_by('-created_at')