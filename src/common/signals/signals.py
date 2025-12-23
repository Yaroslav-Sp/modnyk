from django.apps import apps


def pre_save_category(sender, instance, **kwargs):
    if instance.parent == "":
        instance.level = 0
    else:
        parent = instance.parent
        level = 0
        while parent:
            level += 1
            parent = parent.parent
        instance.level = level


def post_migrate_create_delivery_types(sender, **kwargs):
    DeliveryType = apps.get_model("orders", "DeliveryType")
    if not DeliveryType.objects.exists():
        DeliveryType.objects.create(name="Self-pickup", default_cost=0)
        DeliveryType.objects.create(name="Courier delivery", default_cost=5)
        DeliveryType.objects.create(name="Shipping", default_cost=2)
        DeliveryType.objects.create(name="Postal delivery", default_cost=3)
