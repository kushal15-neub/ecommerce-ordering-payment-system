from django.test import TestCase

from products.models import Category, Product
from products.services import (
    get_all_child_categories,
    get_category_and_children_ids
)


class ProductServiceTests(TestCase):

    def setUp(self):

        self.electronics = Category.objects.create(
            name="Electronics"
        )

        self.laptops = Category.objects.create(
            name="Laptops",
            parent=self.electronics
        )

        self.phones = Category.objects.create(
            name="Phones",
            parent=self.electronics
        )

    def test_dfs_returns_child_categories(self):

        children = get_all_child_categories(
            self.electronics
        )

        names = [cat.name for cat in children]

        self.assertIn("Laptops", names)
        self.assertIn("Phones", names)

    def test_category_ids_include_parent_and_children(self):

        ids = get_category_and_children_ids(
            self.electronics
        )

        self.assertIn(self.electronics.id, ids)
        self.assertIn(self.laptops.id, ids)
        self.assertIn(self.phones.id, ids)

    def test_product_subtotal_on_save(self):

        category = Category.objects.create(name="Test")

        product = Product.objects.create(
            name="Test Product",
            sku="TST-001",
            description="Test",
            price=100,
            stock=10,
            category=category
        )

        self.assertEqual(product.name, "Test Product")
