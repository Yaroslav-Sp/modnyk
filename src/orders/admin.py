from django.contrib import admin

from orders.models import (DeliveryAddress, DeliveryType, Order, OrderItem,
                           Payment)

admin.site.register([Order, OrderItem, DeliveryAddress, Payment, DeliveryType])
