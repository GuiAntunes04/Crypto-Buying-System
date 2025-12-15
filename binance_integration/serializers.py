from rest_framework import serializers
from .models import BinanceKey

class BinanceKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = BinanceKey
        fields = ['api_key']
