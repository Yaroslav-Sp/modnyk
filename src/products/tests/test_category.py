from django.test import TestCase

from products.models import Category


class CategoryModelTest(TestCase):
    def setUp(self):
        self.parent_category = Category.objects.create(name="Clothing", category_level=0)
        self.child_category = Category.objects.create(
            name="Shorts", category_level=1, parent_category=self.parent_category
        )

    def test_category_creation(self):
        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(self.parent_category.name, "Clothing")
        self.assertEqual(self.child_category.parent_category, self.parent_category)
        self.assertEqual(self.child_category.category_level, 1)

    def test_category_str_method(self):
        self.assertEqual(str(self.child_category), f"{self.parent_category} -> {self.child_category.name}")
