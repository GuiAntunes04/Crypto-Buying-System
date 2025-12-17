from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'symbol', 'side', 'quantity', 'status', 'created_at')
    list_filter = ('side', 'status', 'symbol')
