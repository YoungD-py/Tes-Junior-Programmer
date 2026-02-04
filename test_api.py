"""
Script untuk test API eksternal Fast Print
Jalankan: python test_api.py
"""

import requests
import hashlib
from datetime import datetime
import json
import base64

# Configuration
API_URL = "https://recruitment.fastprint.co.id/tes/api_tes_programmer"
# USERNAME akan berubah setiap hari sesuai format: testprogrammerDDMMYYC + counter
# Untuk hari ini (3 Feb 2026) cek dari response header X-Credentials-Username
USERNAME = "tesprogrammer030226C21"  # GANTI SESUAI HEADER RESPONSE

# Generate password: bisacoding-DD-MM-YY
today = datetime.now()
password_format = f"bisacoding-{today.strftime('%d-%m-%y')}"
password_md5 = hashlib.md5(password_format.encode()).hexdigest()

print("=" * 70)
print("TEST API FAST PRINT")
print("=" * 70)
print(f"URL: {API_URL}")
print(f"Username: {USERNAME}")
print(f"Password Format: {password_format}")
print(f"Password MD5: {password_md5}")
print()

# Create Basic Auth header
credentials = f"{USERNAME}:{password_md5}"
encoded = base64.b64encode(credentials.encode()).decode()
headers = {
    'Authorization': f'Basic {encoded}',
    'User-Agent': 'FastPrint-Test/1.0'
}

print("Headers:")
print(f"Authorization: Basic {encoded}")
print()

try:
    print("Sending POST request...")
    
    # Prepare POST data
    post_data = {
        'username': USERNAME,
        'password': password_md5
    }
    
    print(f"POST data: {post_data}\n")
    
    response = requests.post(API_URL, data=post_data, headers=headers, timeout=10, verify=True)
    
    print(f"\nResponse Status: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"Response Cookies: {dict(response.cookies)}")
    
    if response.status_code == 200:
        data = response.json()
        print("\n✅ API Response SUCCESS!")
        print(f"\nData received:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        # Count products
        if isinstance(data, dict) and 'data' in data:
            products = data['data']
            print(f"\n📊 Total products: {len(products)}")
            
            # Show first 3 products
            if products:
                print("\nFirst 3 products:")
                for i, product in enumerate(products[:3], 1):
                    print(f"\n{i}. {product.get('nama_produk', 'N/A')}")
                    print(f"   Kategori: {product.get('kategori', 'N/A')}")
                    print(f"   Harga: {product.get('harga', 'N/A')}")
                    print(f"   Status: {product.get('status', 'N/A')}")
    else:
        print(f"\n❌ API Response ERROR!")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")

except requests.exceptions.ConnectionError:
    print("\n❌ Connection Error - Tidak dapat terhubung ke API")
    print("Periksa koneksi internet Anda")

except requests.exceptions.Timeout:
    print("\n❌ Timeout Error - API tidak merespons dalam waktu yang ditentukan")

except requests.exceptions.HTTPError as e:
    print(f"\n❌ HTTP Error: {e}")

except ValueError as e:
    print(f"\n❌ JSON Decode Error: {e}")
    print(f"Response text: {response.text}")

except Exception as e:
    print(f"\n❌ Error: {str(e)}")

print("\n" + "=" * 70)
