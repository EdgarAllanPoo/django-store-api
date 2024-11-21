from django.test import TestCase
from rest_framework.test import APIClient
from django.core.cache import cache
from .models import Category, Product
from rest_framework import status
from django.utils.http import urlencode

class CategoryViewTests(TestCase):
    def setUp(self):
        # Setup any test data
        self.client = APIClient()
        self.category = Category.objects.create(name="Test Category")
        self.url_list_create = "/api/categories/"  # URL for CategoryListCreate view
        self.url_detail = f"/api/categories/{self.category.pk}/"  # URL for CategoryRetrieveUpdateDestroy view

    def test_category_list_create_get(self):
        # Test GET request for CategoryListCreate
        response = self.client.get(self.url_list_create)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Test Category")

    def test_category_list_create_post(self):
        # Test POST request for CategoryListCreate
        data = {"name": "New Category"}
        response = self.client.post(self.url_list_create, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(response.data["name"], "New Category")

    def test_category_cache(self):
        # Test if cache is used and works correctly
        cache.set("store:categories", [{"name": "Cached Category"}])
        response = self.client.get(self.url_list_create)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["name"], "Cached Category")

    def test_category_cache_clear_on_create(self):
        # Ensure that cache is cleared when a category is created
        cache.set("store:categories", [{"name": "Old Cached Category"}])
        data = {"name": "Another Category"}
        response = self.client.post(self.url_list_create, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(cache.get("store:categories"))

    def test_category_update(self):
        # Test PUT request for CategoryRetrieveUpdateDestroy
        data = {"name": "Updated Category"}
        response = self.client.put(self.url_detail, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, "Updated Category")

    def test_category_delete(self):
        # Test DELETE request for CategoryRetrieveUpdateDestroy
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)

class ProductViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(
            name="Test Product", category=self.category, price=100
        )
        self.url_list_create = "/api/products/"
        self.url_detail = f"/api/products/{self.product.pk}/"

    def test_product_list_create_get(self):
        # Test GET request for ProductListCreate
        response = self.client.get(self.url_list_create)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Test Product")

    def test_product_list_create_post(self):
        # Test POST request for ProductListCreate
        data = {"name": "New Product", "category": self.category.pk, "price": 150}
        response = self.client.post(self.url_list_create, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(response.data["name"], "New Product")

    def test_product_cache(self):
        # Test if cache is used and works correctly for products
        query_params = urlencode({"category__name": "Test Category"})
        cache_key = f"store:products:{query_params}"
        cache.set(cache_key, [{"name": "Cached Product"}])
        response = self.client.get(f"{self.url_list_create}?category__name=Test Category")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["name"], "Cached Product")

    def test_product_cache_clear_on_create(self):
        # Ensure cache is cleared after a new product is created
        cache_key = f"store:products:category__name=TestCategory+Food&price__gte=&price__lte="
        response = self.client.get(f"{self.url_list_create}?category__name=Test Category")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {"name": "Another Product", "category": self.category.pk, "price": 200}
        response = self.client.post(self.url_list_create, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(cache.get(cache_key))

    def test_product_update(self):
        # Test PUT request for ProductRetrieveUpdateDestroy
        data = {"name": "Updated Product", "category": self.category.pk, "price": 120}
        response = self.client.put(self.url_detail, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, "Updated Product")

    def test_product_delete(self):
        # Test DELETE request for ProductRetrieveUpdateDestroy
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)
