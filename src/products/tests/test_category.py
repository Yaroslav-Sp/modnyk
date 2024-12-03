from django.test import TestCase

from products.models import Category
from products.utils.samples_product import sample_category


class CategoryModelTest(TestCase):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)

    def setUp(self):
        self.gender_category = Category.objects.create(name="Men", level=0)
        self.main_category = Category.objects.create(name="Outerwear", level=1, parent=self.gender_category)
        self.subcategory = Category.objects.create(name="Shirts", level=2, parent=self.main_category)

    def test_category_creation(self):
        self.assertEqual(Category.objects.count(), 3)

        self.assertEqual(self.gender_category.name, "Men")
        self.assertEqual(self.main_category.parent, self.gender_category)
        self.assertEqual(self.subcategory.parent, self.main_category)

    def test_sample_category(self):
        sample = sample_category()
        self.assertEqual(sample.name, "Shirts")
        self.assertEqual(sample.parent.name, "Outerwear")
        self.assertEqual(sample.parent.parent.name, "Men")
