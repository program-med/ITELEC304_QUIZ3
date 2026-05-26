from django.test import TestCase
from django.urls import reverse
from .models import Category, Product


class ProductViewsTests(TestCase):
    def setUp(self):
        category = Category.objects.create(name='Office Supplies')
        self.product = Product.objects.create(
            name='Executive Notebook',
            category=category,
            description='A premium notebook for professional teams.',
            price='399.99',
            sku='NB-001',
            available=True,
        )

    def test_product_list_page_renders(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Executive Notebook')

    def test_product_detail_page_renders(self):
        response = self.client.get(self.product.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A premium notebook')
