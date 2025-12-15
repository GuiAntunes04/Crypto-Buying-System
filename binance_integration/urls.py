from django.urls import path
from .views import save_binance_keys, MarketBuyView

urlpatterns = [
    path('keys/', save_binance_keys),
    path('buy/', MarketBuyView.as_view()),
]
