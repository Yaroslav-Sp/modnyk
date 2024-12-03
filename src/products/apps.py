from django.apps import AppConfig
from django.db.models.signals import pre_save


class ProductsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "products"

    def ready(self):
        from common.signals.signals import pre_save_category
        from products.models import Category

        pre_save.connect(receiver=pre_save_category, sender=Category)
