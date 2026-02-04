#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fastprint_project.settings')
django.setup()

from products.services import FastPrintAPIService
from products.models import Product, Kategori, Status

print("Fetching API data...")
api_service = FastPrintAPIService()
api_response = api_service.fetch_products()

print(f"API response data length: {len(api_response.get('data', []))}")
products_data = api_service.parse_product_data(api_response)

print(f"Parsed products length: {len(products_data)}")
print(f"Type of products_data: {type(products_data)}")

if products_data:
    print(f"Type of first item: {type(products_data[0])}")

# Save products to database
saved_count = 0
for i, product_data in enumerate(products_data):
    if not isinstance(product_data, dict):
        print(f"ERROR at index {i}: product_data is {type(product_data)}, value: {product_data}")
        continue
    
    # Get or create kategori
    kategori, _ = Kategori.objects.get_or_create(nama_kategori=product_data['kategori'])
    
    # Get or create status
    status, _ = Status.objects.get_or_create(nama_status=product_data['status'])
    
    # Create or update product
    product, created = Product.objects.update_or_create(
        nama_produk=product_data['nama_produk'],
        defaults={
            'harga': int(product_data['harga']),
            'kategori': kategori,
            'status': status
        }
    )
    if created:
        saved_count += 1

print(f'Successfully saved {saved_count} new products')
print(f'\nDatabase stats:')
print(f'  Products: {Product.objects.count()}')
print(f'  Categories: {Kategori.objects.count()}')
print(f'  Status: {Status.objects.count()}')

# Show "bisa dijual" products only
bisa_dijual_count = Product.objects.filter(status__nama_status='bisa dijual').count()
print(f'  "Bisa dijual": {bisa_dijual_count}')

if Product.objects.count() > 0:
    print("\nSample products (with bisa dijual status):")
    for product in Product.objects.filter(status__nama_status='bisa dijual')[:5]:
        print(f"  - {product.nama_produk} ({product.status}) - Rp {product.harga:,}")
