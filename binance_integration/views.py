from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import BinanceKey
from .serializers import BinanceKeySerializer
from .encryption import encrypt_secret

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_binance_key(request):
    api_key = request.data.get('api_key')
    secret_key = request.data.get('secret_key')

    if not api_key or not secret_key:
        return Response(
            {"error": "api_key and secret_key are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    encrypted_secret = encrypt_secret(secret_key)

    BinanceKey.objects.update_or_create(
        user=request.user,
        defaults={
            'api_key': api_key,
            'secret_key': encrypted_secret
        }
    )

    return Response(
        {"message": "Binance keys saved successfully"},
        status=status.HTTP_201_CREATED
    )

# Create your views here.
