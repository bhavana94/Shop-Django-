from django.contrib import admin
from .models import Seller, Customer, Item, Order, OrderItem

admin.site.register(Seller)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Item)
admin.site.register(OrderItem)
