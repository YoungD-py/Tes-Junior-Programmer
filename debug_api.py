#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fastprint_project.settings')
django.setup()

from products.services import FastPrintAPIService
import json

print("Fetching API data...")
api_service = FastPrintAPIService()
response = api_service.fetch_products()

print(f"API returned: {len(response.get('data', []))} products")

# Parse products
parsed = api_service.parse_product_data(response)
print(f"Parsed returned: {len(parsed)} products")
print(f"Type of parsed: {type(parsed)}")

if parsed:
    print(f"Type of first item: {type(parsed[0])}")
    print(f"First parsed product: {parsed[0]}")
