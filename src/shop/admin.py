from django.contrib import admin

from shop.models import PromotionBanner, Favorite

admin.site.register([PromotionBanner, Favorite])
