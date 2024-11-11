from django.contrib import admin

from products.models import Brand, Category, Color, Product, ProductImage, Size

admin.site.register([Product, ProductImage, Category, Size, Color, Brand])
