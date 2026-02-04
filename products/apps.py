"""
Django apps configuration untuk products app.
"""

from django.apps import AppConfig


class ProductsConfig(AppConfig):
    """
    Configuration untuk app products.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'
    verbose_name = 'Manajemen Produk'
