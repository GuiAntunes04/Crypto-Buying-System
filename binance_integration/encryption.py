from cryptography.fernet import Fernet
from django.conf import settings

def get_fernet():
    return Fernet(settings.FERNET_KEY)

def encrypt_secret(secret: str) -> bytes:
    f = get_fernet()
    return f.encrypt(secret.encode())

def decrypt_secret(token: bytes) -> str:
    f = get_fernet()
    return f.decrypt(token).decode()
