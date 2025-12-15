from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

from .serializers import OrderSerializer
from .services.binance_service import BinanceService
from .models import BinanceKey


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


# 🔹 VIEW DE COMPRA (A SUA, INTACTA)
class MarketBuyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = BinanceService(request.user)

        order = service.buy(
            symbol=serializer.validated_data['symbol'],
            quantity=serializer.validated_data['quantity']
        )

        return Response(order, status=status.HTTP_201_CREATED)
