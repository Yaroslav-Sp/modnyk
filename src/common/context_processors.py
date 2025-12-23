from products.models import Category


def categories_context(request):
    categories = Category.objects.select_related("parent__parent")
    return {
        "genders": categories.filter(level=0),
        "index_categories": categories.filter(level=1).values_list("name", flat=True).distinct(),
    }
