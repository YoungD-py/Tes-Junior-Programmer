#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fastprint_project.settings')
django.setup()

from products.models import Product, Kategori, Status

print(f'Products in DB: {Product.objects.count()}')
print(f'Categories in DB: {Kategori.objects.count()}')
print(f'Status in DB: {Status.objects.count()}')

if Product.objects.count() > 0:
    print("\nSample products:")
    for product in Product.objects.all()[:3]:
        print(f"  - {product.nama_produk} ({product.status})")
