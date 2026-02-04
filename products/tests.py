"""
Tests untuk products app.
"""

from django.test import TestCase
from django.test import Client
from .models import Product, Kategori, Status


class KategoriModelTest(TestCase):
    """Test untuk model Kategori."""

    def setUp(self):
        self.kategori = Kategori.objects.create(nama_kategori="Kertas")

    def test_kategori_creation(self):
        """Test creation Kategori."""
        self.assertEqual(self.kategori.nama_kategori, "Kertas")
        self.assertTrue(self.kategori.id_kategori)

    def test_kategori_str(self):
        """Test string representation."""
        self.assertEqual(str(self.kategori), "Kertas")


class StatusModelTest(TestCase):
    """Test untuk model Status."""

    def setUp(self):
        self.status = Status.objects.create(nama_status="bisa dijual")

    def test_status_creation(self):
        """Test creation Status."""
        self.assertEqual(self.status.nama_status, "bisa dijual")
        self.assertTrue(self.status.id_status)

    def test_status_str(self):
        """Test string representation."""
        self.assertEqual(str(self.status), "bisa dijual")


class ProductModelTest(TestCase):
    """Test untuk model Product."""

    def setUp(self):
        self.kategori = Kategori.objects.create(nama_kategori="Kertas")
        self.status = Status.objects.create(nama_status="bisa dijual")
        self.product = Product.objects.create(
            nama_produk="Kertas A4",
            harga=50000,
            kategori=self.kategori,
            status=self.status
        )

    def test_product_creation(self):
        """Test creation Product."""
        self.assertEqual(self.product.nama_produk, "Kertas A4")
        self.assertEqual(self.product.harga, 50000)
        self.assertTrue(self.product.id_produk)

    def test_product_str(self):
        """Test string representation."""
        self.assertEqual(str(self.product), "Kertas A4")

    def test_product_foreign_keys(self):
        """Test foreign key relationships."""
        self.assertEqual(self.product.kategori, self.kategori)
        self.assertEqual(self.product.status, self.status)


class ProductViewTest(TestCase):
    """Test untuk views."""

    def setUp(self):
        self.client = Client()
        self.kategori = Kategori.objects.create(nama_kategori="Kertas")
        self.status = Status.objects.create(nama_status="bisa dijual")
        self.product = Product.objects.create(
            nama_produk="Kertas A4",
            harga=50000,
            kategori=self.kategori,
            status=self.status
        )

    def test_product_list_view(self):
        """Test product list view."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_product_create_view(self):
        """Test product create view."""
        response = self.client.get('/products/create/')
        self.assertEqual(response.status_code, 200)

    def test_product_detail_view(self):
        """Test product detail view."""
        response = self.client.get(f'/products/{self.product.id_produk}/')
        self.assertEqual(response.status_code, 200)
