from django.apps import AppConfig
from django.db.models.signals import post_migrate


class OrdersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "orders"

    def ready(self):
        from common.signals.signals import post_migrate_create_delivery_types

        post_migrate.connect(post_migrate_create_delivery_types, sender=self)
