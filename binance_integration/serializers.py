from rest_framework import serializers
from .models import BinanceKey
from .models import Order

class BinanceKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = BinanceKey
        fields = ['api_key']

class OrderSerializer(serializers.Serializer):
    symbol = serializers.CharField()
    quantity = serializers.DecimalField(max_digits=18, decimal_places=8)

class OrderResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
