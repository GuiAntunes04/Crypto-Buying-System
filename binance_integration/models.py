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
