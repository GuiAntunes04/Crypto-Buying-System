from django.urls import path
from .views import save_binance_keys, MarketBuyView, OrderListView

urlpatterns = [
    path('keys/', save_binance_keys),
    path('buy/', MarketBuyView.as_view()),
    path('orders/', OrderListView.as_view()),
]
