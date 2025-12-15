from django.urls import path
from .views import save_binance_key

urlpatterns = [
    path('keys/', save_binance_key),
]
