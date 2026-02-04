# 📚 DOKUMENTASI TEKNIS - Fast Print Django Application

## 1️⃣ MODELS.PY - Database Models

### Fungsi Utama:
Mendefinisikan struktur database dan relasi antar tabel.

### Models:

#### **Kategori Model**
```python
class Kategori(models.Model):
    id_kategori = AutoField(primary_key=True)
    nama_kategori = CharField(unique=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```
**Penjelasan:**
- Primary key: id_kategori (auto increment)
- nama_kategori: Unique constraint, tidak ada 2 kategori dengan nama sama
- Timestamps: Mencatat kapan data dibuat dan diperbarui

#### **Status Model**
```python
class Status(models.Model):
    id_status = AutoField(primary_key=True)
    nama_status = CharField(unique=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```
**Penjelasan:**
- Struktur sama seperti Kategori
- Menyimpan status produk: "bisa dijual", "tidak tersedia", dll

#### **Product Model**
```python
class Product(models.Model):
    id_produk = AutoField(primary_key=True)
    nama_produk = CharField(required=True)
    harga = DecimalField(max_digits=15, decimal_places=2)
    kategori = ForeignKey(Kategori, on_delete=models.PROTECT)
    status = ForeignKey(Status, on_delete=models.PROTECT)
    deskripsi = TextField(optional)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```
**Penjelasan:**
- Foreign Keys: PROTECT (tidak bisa delete Kategori/Status jika ada produk)
- DecimalField lebih cocok untuk harga (akurat)
- related_name='products' untuk reverse query

---

## 2️⃣ SERIALIZERS.PY - DRF Serializers

### Fungsi Utama:
Konversi model Django ke JSON dan sebaliknya, plus validasi data.

### Serializers:

#### **KategoriSerializer**
- Converts Kategori model ↔ JSON
- Fields: id_kategori, nama_kategori, created_at, updated_at

#### **StatusSerializer**
- Converts Status model ↔ JSON
- Fields: id_status, nama_status, created_at, updated_at

#### **ProductSerializer**
```python
class ProductSerializer(serializers.ModelSerializer):
    kategori_detail = KategoriSerializer(source='kategori', read_only=True)
    status_detail = StatusSerializer(source='status', read_only=True)
```
**Fitur:**
- Nested serializers untuk kategori dan status
- Custom validation methods:
  - `validate_nama_produk()`: Cek tidak kosong
  - `validate_harga()`: Cek positif

#### **ProductCreateUpdateSerializer**
**Perbedaan dari ProductSerializer:**
- Lebih ketat untuk input user
- Validasi nama_produk minimal 3 karakter
- Harga harus positif dan numeric

**Keuntungan:**
- Separation of concerns (read vs write)
- Lebih mudah maintain validasi

---

## 3️⃣ VIEWS.PY - Request Handlers

### Tipe Views:

#### **REST API Views (ViewSets)**

##### ProductViewSet
```
GET    /api/products/                    - List all (status="bisa dijual")
POST   /api/products/                    - Create new
GET    /api/products/{id}/               - Retrieve
PUT    /api/products/{id}/               - Full update
PATCH  /api/products/{id}/               - Partial update
DELETE /api/products/{id}/               - Delete

Custom Actions:
GET    /api/products/fetch_from_api/     - Fetch dari API eksternal
GET    /api/products/by_kategori/        - Filter by kategori
```

**Fitur Filtering:**
```python
def get_queryset(self):
    queryset = Product.objects.filter(status__nama_status='bisa dijual')
    
    if kategori_filter:
        queryset = queryset.filter(kategori__id_kategori=kategori_filter)
    
    if search:
        queryset = queryset.filter(nama_produk__icontains=search)
    
    return queryset
```

##### Custom Action: fetch_from_api
```python
@action(detail=False, methods=['get'])
def fetch_from_api(self, request):
    # 1. Get username dari query params
    # 2. Fetch dari API eksternal
    # 3. Parse data
    # 4. Save ke database
    # 5. Return response
```

#### **Web Views (Function-Based)**

##### product_list()
- Display daftar produk (hanya status "bisa dijual")
- Support pagination (10 per page)
- Support search by nama_produk
- Support filter by kategori
- Template: product_list.html

##### product_create()
- Display form tambah produk
- Validasi input (nama_produk, harga)
- Save ke database jika valid
- Redirect ke product_list dengan success message

##### product_update()
- Display form edit (pre-populated)
- Validasi input
- Update database
- Redirect ke product_detail

##### product_delete()
- Display halaman konfirmasi
- Jika confirmed: delete dan redirect ke product_list
- Jika cancel: redirect ke product_detail

##### product_detail()
- Display detail produk
- Show semua field termasuk timestamps

##### fetch_api_data()
- Display form untuk input username
- Fetch dari API eksternal
- Parse dan save ke database
- Show success/error message

---

## 4️⃣ SERVICES.PY - API Eksternal Service

### Fungsi Utama:
Menangani komunikasi dengan API eksternal Fast Print.

### Class: FastPrintAPIService

#### Method: generate_password()
```python
def generate_password() -> str:
    # Format: bisacoding-DD-MM-YY
    # Contoh: bisacoding-03-02-26 (untuk 3 Feb 2026)
    # Return: MD5 hash dari string tersebut
```

**Implementasi:**
```python
today = datetime.now()
password_format = f"bisacoding-{today.strftime('%d-%m-%y')}"
md5_hash = hashlib.md5(password_format.encode()).hexdigest()
```

#### Method: get_auth_headers(username)
```python
def get_auth_headers(username) -> Dict:
    # 1. Generate password (MD5)
    # 2. Buat credentials: "username:password"
    # 3. Base64 encode
    # 4. Return: {'Authorization': 'Basic <encoded>'}
```

#### Method: fetch_products(username)
```python
def fetch_products(username) -> Dict:
    # 1. Get auth headers
    # 2. HTTP GET ke API
    # 3. Handle berbagai exceptions:
    #    - ConnectionError
    #    - Timeout
    #    - HTTPError (401, 403, etc)
    #    - JSON decode error
    # 4. Log response headers & cookies
    # 5. Return parsed JSON
```

**Error Handling:**
```python
try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return response.json()
except requests.exceptions.ConnectionError:
    raise Exception("Tidak dapat terhubung ke API")
except requests.exceptions.Timeout:
    raise Exception("Request timeout")
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 401:
        raise Exception("Autentikasi gagal")
    elif e.response.status_code == 403:
        raise Exception("Anda tidak memiliki akses")
```

#### Method: parse_product_data(api_response)
```python
def parse_product_data(api_response) -> List[Dict]:
    # 1. Extract data array dari response
    # 2. Iterate setiap item
    # 3. Validasi: nama_produk & harga > 0
    # 4. Return list of valid products
```

**Contoh Response:**
```json
{
    "data": [
        {
            "nama_produk": "Kertas A4",
            "harga": 50000,
            "kategori": "Kertas",
            "status": "bisa dijual"
        }
    ]
}
```

---

## 5️⃣ FORMS.PY - Form Validation

### Fungsi Utama:
Validasi input dari user untuk create/update produk.

### ProductForm

**Widgets:**
```python
nama_produk = TextInput(attrs={
    'class': 'form-control',
    'placeholder': 'Masukkan nama produk',
    'required': True,
})

harga = NumberInput(attrs={
    'class': 'form-control',
    'min': '0',
    'step': '0.01',
})
```

**Custom Validators:**

#### clean_nama_produk()
```python
def clean_nama_produk(self):
    nama = self.cleaned_data.get('nama_produk', '').strip()
    
    if not nama:
        raise ValidationError('Nama produk tidak boleh kosong')
    
    if len(nama) < 3:
        raise ValidationError('Nama produk minimal 3 karakter')
    
    if len(nama) > 255:
        raise ValidationError('Nama produk maksimal 255 karakter')
    
    return nama
```

#### clean_harga()
```python
def clean_harga(self):
    harga = self.cleaned_data.get('harga')
    
    if harga is None:
        raise ValidationError('Harga tidak boleh kosong')
    
    try:
        harga_float = float(harga)
    except (ValueError, TypeError):
        raise ValidationError('Harga harus berupa angka')
    
    if harga_float <= 0:
        raise ValidationError('Harga harus lebih besar dari 0')
    
    return harga
```

---

## 6️⃣ URLS.PY - URL Routing

### URL Patterns:

#### Web Routes
```
/                           → product_list
/products/create/           → product_create
/products/<id>/             → product_detail
/products/<id>/update/      → product_update
/products/<id>/delete/      → product_delete
/fetch-api/                 → fetch_api_data
```

#### API Routes
```
/api/products/              → ProductViewSet (list/create)
/api/products/<id>/         → ProductViewSet (retrieve/update/delete)
/api/products/fetch_from_api/ → Custom action
/api/kategoris/             → KategoriViewSet (readonly)
/api/statuses/              → StatusViewSet (readonly)
/api-auth/                  → DRF auth URLs
```

---

## 7️⃣ TEMPLATES - UI Components

### Base Template (base.html)
- Navbar dengan links ke semua fitur
- Messages display (success/error/info)
- Footer
- Bootstrap 5 styling
- Custom CSS variables

### product_list.html
**Fitur:**
- Grid layout untuk produk
- Search input (real-time filter)
- Kategori dropdown filter
- Pagination (10 per page)
- Card design untuk setiap produk
- Buttons: View, Edit, Delete
- Message jika tidak ada produk

**Filter Logic:**
```html
<form method="get">
    <input name="search" value="{{ search_query }}">
    <select name="kategori">
        <option value="{{ kategori_filter }}">...
    </select>
</form>
```

### product_form.html
**Form Fields:**
- nama_produk: TextInput (required)
- harga: NumberInput (required)
- kategori: Select dropdown (required)
- status: Select dropdown (required)
- deskripsi: Textarea (optional)

**Validasi Display:**
```html
{% if form.nama_produk.errors %}
    <div class="invalid-feedback d-block">
        {% for error in form.nama_produk.errors %}
            {{ error }}<br>
        {% endfor %}
    </div>
{% endif %}
```

### product_detail.html
- Table layout untuk detail
- Formatted currency (Rp)
- Timestamps display
- Action buttons

### product_confirm_delete.html
- Alert dengan warning icon
- Product details preview
- Confirm/Cancel buttons
- JavaScript confirm() popup

### fetch_api.html
- Info box tentang API
- Username input (default: "user")
- Sync button dengan confirmation
- Documentation section

---

## 8️⃣ SETTINGS.PY - Configuration

### Database
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'fastprint_db',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Installed Apps
```python
INSTALLED_APPS = [
    # Django defaults
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party
    'rest_framework',
    
    # Local
    'products',
]
```

### Templates
```python
TEMPLATES = [
    {
        'DIRS': [BASE_DIR / 'templates'],  # Global templates
        'APP_DIRS': True,                   # products/templates/
    }
]
```

### REST Framework
```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}
```

### Internationalization
```python
LANGUAGE_CODE = 'id-ID'
TIME_ZONE = 'Asia/Jakarta'
USE_I18N = True
USE_TZ = True
```

---

## 🎯 FLOW DIAGRAM

### Flow: Create Product

```
User Form
   ↓
product_create() view
   ↓
ProductForm validation
   ↓
Models saved to DB
   ↓
Success message
   ↓
Redirect product_list
```

### Flow: Fetch API Data

```
fetch_api_data() page
   ↓
User submit username
   ↓
FastPrintAPIService.fetch_products()
   ↓
Generate auth header (MD5 password)
   ↓
HTTP request to API
   ↓
Parse response
   ↓
Create/Update Kategori & Status
   ↓
Create/Update Product
   ↓
Success message
   ↓
Redirect product_list
```

### Flow: Delete Product (Confirmation)

```
User click delete
   ↓
product_delete() → confirm page
   ↓
User confirm
   ↓
JavaScript confirm()
   ↓
POST delete
   ↓
Product.delete()
   ↓
Success message
   ↓
Redirect product_list
```

---

## 🔍 VALIDATION RULES

### Form Level (forms.py)
- nama_produk: required, 3-255 chars
- harga: required, numeric, > 0
- kategori: required
- status: required

### Serializer Level (serializers.py)
- nama_produk: not empty
- harga: numeric, >= 0

### Database Level (models.py)
- nama_kategori: unique
- nama_status: unique
- harga: max 15 digits, 2 decimal places

---

## 💾 DATABASE OPERATIONS

### Create
```python
Product.objects.create(
    nama_produk="Kertas A4",
    harga=50000,
    kategori=kategori_obj,
    status=status_obj
)
```

### Read
```python
Product.objects.filter(status__nama_status='bisa dijual')
Product.objects.get(id_produk=1)
Product.objects.select_related('kategori', 'status')
```

### Update
```python
Product.objects.filter(id_produk=1).update(harga=55000)
# atau
product.harga = 55000
product.save()
```

### Delete
```python
Product.objects.get(id_produk=1).delete()
```

---

## 🧪 TESTING

### Unit Test: Models
```python
def test_product_creation(self):
    product = Product.objects.create(...)
    self.assertEqual(product.nama_produk, "Kertas A4")
```

### Unit Test: Views
```python
def test_product_list_view(self):
    response = self.client.get('/')
    self.assertEqual(response.status_code, 200)
```

### Run Tests
```bash
python manage.py test products
python manage.py test products.tests.ProductViewTest
```

---

## 🚀 DEPLOYMENT CHECKLIST

- [ ] Set DEBUG = False
- [ ] Update ALLOWED_HOSTS
- [ ] Use environment variables untuk secrets
- [ ] Collect static files: `python manage.py collectstatic`
- [ ] Run migrations: `python manage.py migrate`
- [ ] Create superuser untuk admin
- [ ] Test semua endpoints
- [ ] Setup SSL certificate
- [ ] Configure CORS (jika needed)
- [ ] Add logging dan monitoring

---

## 📋 SUMMARY

| File | Fungsi |
|------|--------|
| models.py | Database schema |
| serializers.py | JSON conversion + validation |
| views.py | Request handlers (Web + API) |
| forms.py | Form validation |
| services.py | External API communication |
| urls.py | URL routing |
| templates/ | UI components |
| admin.py | Django admin interface |
| settings.py | Django configuration |

Semua file dirancang dengan prinsip clean code, separation of concerns, dan beginner-friendly! 🎯
