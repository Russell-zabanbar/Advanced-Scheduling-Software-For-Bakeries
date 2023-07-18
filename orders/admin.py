from django.contrib import admin
from orders.models import Order, ReadyOrders, StoreBaker

admin.site.register(Order)
admin.site.register(ReadyOrders)
admin.site.register(StoreBaker)