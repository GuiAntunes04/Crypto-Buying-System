from django.db import models
from django.contrib.auth.models import User

class BinanceKey(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    api_key = models.CharField(max_length=255)
    secret_key = models.BinaryField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"BinanceKey - {self.user.username}"
