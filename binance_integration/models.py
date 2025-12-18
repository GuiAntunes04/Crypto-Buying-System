from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
from django.conf import settings

cipher = Fernet(settings.FERNET_KEY)


class BinanceKey(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    api_key = models.CharField(max_length=255)
    secret_key = models.BinaryField()

    def set_secret_key(self, raw_secret: str):
        self.secret_key = cipher.encrypt(raw_secret.encode())

    def get_secret_key(self) -> str:
        return cipher.decrypt(self.secret_key).decode()

from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    SIDE_CHOICES = (
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=20)
    side = models.CharField(max_length=4, choices=SIDE_CHOICES)

    order_id = models.BigIntegerField()
    price = models.DecimalField(max_digits=18, decimal_places=8)
    quantity = models.DecimalField(max_digits=18, decimal_places=8)
    quote_quantity = models.DecimalField(max_digits=18, decimal_places=8)

    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    raw_response = models.JSONField()

    class Meta:
        indexes = [
            models.Index(fields=['user', 'symbol']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.symbol} {self.side} #{self.order_id}"

