# ⚡ QUICK REFERENCE GUIDE

## 🎯 Untuk Junior Programmer - Panduan Cepat

---

## 1️⃣ SETUP CEPAT (5 menit)

```bash
# Buka terminal di project folder
cd d:\fastPrint\fastprint_project

# Aktifkan virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Edit settings.py - ganti database credentials
# Buka: fastprint_project/settings.py
# Cari bagian DATABASES dan sesuaikan

# Jalankan migrations
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Jalankan server
python manage.py runserver

# Buka browser: http://localhost:8000
```

---

## 2️⃣ STRUKTUR FILE PENTING

```
products/
├── models.py          ← Database structure (Kategori, Status, Product)
├── views.py           ← Business logic (CRUD operations)
├── serializers.py     ← API data conversion (DRF)
├── forms.py           ← Form validation
├── services.py        ← External API integration
├── urls.py            ← URL routing
├── admin.py           ← Admin panel config
└── templates/
    └── products/      ← HTML templates
        ├── base.html  ← Base template
        ├── product_list.html
        ├── product_form.html
        ├── product_detail.html
        └── product_confirm_delete.html
```

---

## 3️⃣ ALUR KERJA APLIKASI

### Flow: Lihat Produk
```
User visit /
  ↓
product_list() view
  ↓
Filter: status = "bisa dijual"
  ↓
Tampilkan di product_list.html
  ↓
User lihat products dengan cards
```

### Flow: Tambah Produk
```
User click "Tambah Produk"
  ↓
product_create() view (GET)
  ↓
Tampilkan form kosong
  ↓
User isi form & submit
  ↓
ProductForm validation
  ↓
Jika valid: save ke database
Jika invalid: tampilkan error
  ↓
Redirect ke product_list
```

### Flow: Sinkronisasi API
```
User buka /fetch-api/
  ↓
Tampilkan form input username
  ↓
User submit username
  ↓
FastPrintAPIService.fetch_products()
  ↓
  1. Generate MD5 password (bisacoding-DD-MM-YY)
  2. Create Basic Auth header
  3. HTTP GET ke API eksternal
  ↓
Parse response JSON
  ↓
Create/Update Kategori
Create/Update Status
Create/Update Products
  ↓
Show success message
Redirect ke product_list
```

---

## 4️⃣ VALIDASI FORM

### Validasi yang Ada:
```python
# nama_produk
- Required ✓
- Min 3 karakter ✓
- Max 255 karakter ✓

# harga
- Required ✓
- Must be numeric ✓
- Must be positive (> 0) ✓

# kategori
- Required ✓

# status
- Required ✓
```

### Error Messages:
```
"Nama produk tidak boleh kosong"
"Nama produk minimal 3 karakter"
"Harga harus berupa angka"
"Harga harus lebih besar dari 0"
"Kategori harus dipilih"
"Status harus dipilih"
```

---

## 5️⃣ URL ENDPOINTS

### Web Pages
```
GET  /                     → Daftar produk (home)
GET  /products/create/     → Form tambah
POST /products/create/     → Submit tambah
GET  /products/1/          → Detail produk
GET  /products/1/update/   → Form edit
POST /products/1/update/   → Submit edit
GET  /products/1/delete/   → Konfirmasi hapus
POST /products/1/delete/   → Submit hapus
GET  /fetch-api/           → Sinkronisasi API
```

### REST API
```
GET    /api/products/              → Daftar
POST   /api/products/              → Buat
GET    /api/products/1/            → Detail
PUT    /api/products/1/            → Update
DELETE /api/products/1/            → Hapus
GET    /api/products/fetch_from_api/?username=user → Sync
```

---

## 6️⃣ DATABASE OPERATIONS

### Create
```python
from products.models import Product, Kategori, Status

kategori = Kategori.objects.create(nama_kategori="Kertas")
status = Status.objects.create(nama_status="bisa dijual")

product = Product.objects.create(
    nama_produk="Kertas A4",
    harga=50000,
    kategori=kategori,
    status=status,
    deskripsi="Kertas berkualitas"
)
```

### Read
```python
# Get all
products = Product.objects.all()

# Get one
product = Product.objects.get(id_produk=1)

# Filter
products = Product.objects.filter(status__nama_status='bisa dijual')

# Search
products = Product.objects.filter(nama_produk__icontains='Kertas')
```

### Update
```python
# Method 1
product = Product.objects.get(id_produk=1)
product.harga = 55000
product.save()

# Method 2
Product.objects.filter(id_produk=1).update(harga=55000)
```

### Delete
```python
# Method 1
product = Product.objects.get(id_produk=1)
product.delete()

# Method 2
Product.objects.filter(id_produk=1).delete()

# All
Product.objects.all().delete()
```

---

## 7️⃣ DJANGO SHELL

```bash
# Buka interactive Python shell
python manage.py shell

# Di dalam shell:
from products.models import Product, Kategori, Status

# Check data
print(Product.objects.all().count())

# Create
Product.objects.create(nama_produk="Test", harga=100, ...)

# Exit
exit()
```

---

## 8️⃣ COMMON COMMANDS

```bash
# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Change password
python manage.py changepassword admin

# Backup data
python manage.py dumpdata > backup.json

# Restore data
python manage.py loaddata backup.json

# Run tests
python manage.py test

# Collect static files
python manage.py collectstatic

# Check errors
python manage.py check

# Deploy check
python manage.py check --deploy

# Clear database
python manage.py flush
```

---

## 9️⃣ API AUTHENTICATION

### Basic Auth Header
```python
import base64

username = "user"
password = "md5_hash"  # Generated from bisacoding-DD-MM-YY

credentials = f"{username}:{password}"
encoded = base64.b64encode(credentials.encode()).decode()

headers = {
    'Authorization': f'Basic {encoded}'
}
```

### Password Generation
```python
import hashlib
from datetime import datetime

today = datetime.now()
password_format = f"bisacoding-{today.strftime('%d-%m-%y')}"
md5_hash = hashlib.md5(password_format.encode()).hexdigest()
```

---

## 🔟 JAVASCRIPT DELETE CONFIRMATION

### Simple Alert
```html
<a href="/products/1/delete/" onclick="return confirmDelete()">
    Delete
</a>

<script>
function confirmDelete() {
    return confirm('Yakin ingin hapus?');
}
</script>
```

### With Details
```html
<a href="/products/1/delete/" 
   onclick="return confirm('Hapus: Kertas A4?')">
    Delete
</a>
```

### Inline in Template
```html
<a href="{% url 'product_delete' product.id_produk %}" 
   onclick="return confirmDelete()">
    🗑️ Hapus
</a>
```

---

## 1️⃣1️⃣ TIPS & TRICKS

### Query Optimization
```python
# BAD: N+1 queries
for product in Product.objects.all():
    print(product.kategori.nama_kategori)

# GOOD: Use select_related
for product in Product.objects.select_related('kategori'):
    print(product.kategori.nama_kategori)
```

### Filtering
```python
# Exact match
Product.objects.filter(id_produk=1)

# Contains (case-insensitive)
Product.objects.filter(nama_produk__icontains='Kertas')

# Greater than
Product.objects.filter(harga__gt=50000)

# Less than
Product.objects.filter(harga__lt=50000)

# In list
Product.objects.filter(id_produk__in=[1, 2, 3])

# Exclude
Product.objects.exclude(status__nama_status='tidak tersedia')
```

### Pagination
```python
from django.core.paginator import Paginator

products = Product.objects.all()
paginator = Paginator(products, 10)

page_number = request.GET.get('page', 1)
page_obj = paginator.get_page(page_number)

# In template
{% for product in page_obj %}
    ...
{% endfor %}
```

---

## 1️⃣2️⃣ ERROR HANDLING

### Try-Except in Views
```python
try:
    api_response = FastPrintAPIService.fetch_products(username)
    # ... do something
except Exception as e:
    messages.error(request, f'Error: {str(e)}')
    return redirect('home')
```

### Form Validation Errors
```python
if request.method == 'POST':
    form = ProductForm(request.POST)
    
    if form.is_valid():
        form.save()
    else:
        for field, errors in form.errors.items():
            for error in errors:
                print(f"{field}: {error}")
```

### API Error Handling
```python
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
except requests.exceptions.ConnectionError:
    print("Cannot connect to API")
except requests.exceptions.Timeout:
    print("API request timeout")
except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e.response.status_code}")
```

---

## 1️⃣3️⃣ DEBUGGING

### Print Debug Info
```python
from django.conf import settings

if settings.DEBUG:
    print(f"Product: {product}")
    print(f"Kategori: {product.kategori.nama_kategori}")
```

### Django Debug Toolbar (optional)
```python
# Install
pip install django-debug-toolbar

# Add to INSTALLED_APPS
INSTALLED_APPS = [..., 'debug_toolbar']

# Add to urls.py
urlpatterns = [..., path('__debug__/', include('debug_toolbar.urls'))]
```

### Logging
```python
import logging

logger = logging.getLogger(__name__)

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

---

## 1️⃣4️⃣ TESTING

### Run Tests
```bash
# All tests
python manage.py test

# Specific app
python manage.py test products

# Specific class
python manage.py test products.tests.ProductModelTest

# Specific method
python manage.py test products.tests.ProductModelTest.test_product_creation

# Verbose
python manage.py test -v 2
```

### Example Test
```python
from django.test import TestCase
from products.models import Product, Kategori, Status

class ProductModelTest(TestCase):
    def setUp(self):
        self.kategori = Kategori.objects.create(nama_kategori="Kertas")
        self.status = Status.objects.create(nama_status="bisa dijual")
    
    def test_product_creation(self):
        product = Product.objects.create(
            nama_produk="Kertas A4",
            harga=50000,
            kategori=self.kategori,
            status=self.status
        )
        self.assertEqual(product.nama_produk, "Kertas A4")
        self.assertEqual(product.harga, 50000)
```

---

## 1️⃣5️⃣ TROUBLESHOOTING QUICK FIX

| Problem | Solution |
|---------|----------|
| ModuleNotFoundError | `pip install -r requirements.txt` |
| Database error | Update credentials di settings.py |
| No migrations | `python manage.py makemigrations && python manage.py migrate` |
| Port already in use | `python manage.py runserver 8080` |
| Template not found | Check TEMPLATES['DIRS'] di settings.py |
| Static files not loading | `python manage.py collectstatic` |
| Cannot import module | Check INSTALLED_APPS di settings.py |

---

## 📚 DOKUMENTASI FILES

| File | Konten |
|------|--------|
| README.md | Overview & features |
| DOKUMENTASI_TEKNIS.md | Technical details (8 sections) |
| SETUP_GUIDE.md | Step-by-step installation |
| FILE_SUMMARY.md | File structure & summary |
| QUICK_REFERENCE.md | (File ini) |

---

## 🎓 LEARNING PATH

### Day 1: Setup
- [ ] Install Python & PostgreSQL
- [ ] Clone project & install dependencies
- [ ] Configure database
- [ ] Run migrations & create superuser

### Day 2: Understanding
- [ ] Read models.py
- [ ] Read views.py
- [ ] Read templates
- [ ] Test CRUD operations

### Day 3: Modification
- [ ] Add new field ke Product
- [ ] Create new validation
- [ ] Modify template
- [ ] Add new view

### Day 4: API
- [ ] Test REST API endpoints
- [ ] Test API synchronization
- [ ] Create custom API action
- [ ] Add API authentication

### Day 5: Testing & Deployment
- [ ] Write unit tests
- [ ] Run all tests
- [ ] Check code quality
- [ ] Deploy to server (optional)

---

## 🚀 PRODUCTION CHECKLIST

- [ ] Set DEBUG = False
- [ ] Update ALLOWED_HOSTS
- [ ] Use environment variables untuk secrets
- [ ] Setup HTTPS/SSL
- [ ] Configure database backups
- [ ] Setup logging
- [ ] Run `python manage.py check --deploy`
- [ ] Collect static files
- [ ] Setup email backend
- [ ] Monitor application
- [ ] Add rate limiting
- [ ] Setup monitoring & alerts

---

**Butuh bantuan? Baca DOKUMENTASI_TEKNIS.md atau SETUP_GUIDE.md!** 

**Happy coding! 🚀**
