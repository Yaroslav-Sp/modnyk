from django.contrib import admin

from shop.models import Favorite, PromotionBanner

admin.site.register([PromotionBanner, Favorite])
