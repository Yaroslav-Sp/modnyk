from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.status import HTTP_403_FORBIDDEN
from rest_framework.test import APIClient

from products.utils.samples_product import sample_category, sample_product


class TestApi(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = sample_category()
        self.product = sample_product(category=self.category)

        self.user = get_user_model()(email="user@example.com")
        self.user.set_password("qwerty1234")
        self.user.save()

    def test_product_details(self):
        self.user.is_superuser = True
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            reverse("api:product_details", kwargs={"category_pk": self.category.pk, "product_pk": self.product.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "name": "TestProduct",
                "description": "This is a test product description.",
                "category": {
                    "name": "Shirts",
                    "level": "Type clothes",
                    "parent": "Outerwear",
                },
                "color": {"name": "Red"},
                "size": [{"name": "M", "description": "Medium size"}],
                "price": "9.99",
                "brand": {"name": "TestBrand"},
            },
        )

    def test_product_details_no_access(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            reverse("api:product_details", kwargs={"category_pk": self.category.pk, "product_pk": self.product.pk})
        )

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data,
            second={
                "detail": ErrorDetail(
                    string="You do not have permission to perform this action.", code="permission_denied"
                )
            },
        )

    def test_product_list_unauthorized_customer(self):
        response = self.client.get(reverse("api:product_list"))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data,
            second={
                "detail": ErrorDetail(string="Authentication credentials were not provided.", code="not_authenticated")
            },
        )

    def test_product_list(self):
        self.user.is_superuser = True
        self.client.force_authenticate(user=self.user)

        response = self.client.get(reverse("api:product_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            [
                {
                    "name": "TestProduct",
                    "description": "This is a test product description.",
                    "category": {
                        "name": "Shirts",
                        "level": "Type clothes",
                        "parent": "Outerwear",
                    },
                    "color": {"name": "Red"},
                    "size": [{"name": "M", "description": "Medium size"}],
                    "price": "9.99",
                    "brand": {"name": "TestBrand"},
                }
            ],
        )

    def test_delete_product(self):
        self.user.is_superuser = True
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse("api:delete_product", kwargs={"pk": self.product.pk}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)

    def test_create_product(self):
        self.user.is_superuser = True
        self.client.force_authenticate(user=self.user)

        product_data = {
            "name": "Jake Polo shirt",
            "description": "Some long text",
            "category": 1,
            "color": 1,
            "size": [1],
            "price": "99.99",
            "brand": 1,
        }

        response = self.client.post(
            reverse("api:create_product"),
            product_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, product_data)

    def test_update_product(self):
        self.user.is_superuser = True
        self.client.force_authenticate(user=self.user)

        data_for_update = {"name": "Updated test name"}

        response = self.client.patch(
            reverse("api:update_product", kwargs={"pk": self.product.pk}),
            data_for_update,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated test name")
