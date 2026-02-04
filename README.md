# 🖨️ Fast Print Indonesia - Product Management System

Aplikasi Django profesional untuk manajemen produk Fast Print Indonesia dengan CRUD lengkap, integrasi API real-time, dan design modern internasional standard.

## ✨ Fitur Utama

- ✅ **API Integration** - Sinkronisasi otomatis dari API eksternal (30 produk)
- ✅ **Modern UI** - Design profesional dengan gradient, animations, dan responsive layout
- ✅ **CRUD Operations** - Create, Read, Update, Delete dengan validasi form
- ✅ **Smart Filtering** - Hanya tampilkan produk status "bisa dijual"
- ✅ **Delete Confirmation** - Dialog konfirmasi sebelum hapus
- ✅ **Form Validation** - Validasi nama & harga otomatis
- ✅ **REST API** - DRF endpoints untuk integrasi frontend/mobile
- ✅ **Admin Panel** - Django admin dengan data management lengkap
- ✅ **PostgreSQL** - Database relasional yang powerful
- ✅ **Responsive Design** - Mobile-first design approach

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd fastprint_project
pip install -r requirements.txt
```

### 2. Setup Database
```bash
# PostgreSQL harus sudah running
python manage.py migrate
python manage.py createsuperuser  # (opsional, jika mau reset admin)
```

### 3. Sinkronisasi API Data
```bash
python sync_api.py
```

### 4. Run Server
```bash
python manage.py runserver
```

### 5. Access Application
- **Produk List**: http://localhost:8000/products/
- **Admin Panel**: http://localhost:8000/admin/
- **REST API**: http://localhost:8000/api/products/

**Default Admin:**
- Username: `admin` atau `badfellas`
- Password: Sesuai yang dibuat saat setup

## 📋 Requirements Completion

| # | Requirement | Status | Lokasi |
|---|---|---|---|
| 1 | Ambil data dari API | ✅ | `products/services.py` |
| 2 | Database 3 tabel | ✅ | `products/models.py` - 30 produk, 7 kategori, 2 status |
| 3 | Simpan produk dari API | ✅ | `sync_api.py` - Automatic import |
| 4 | Halaman tampil data | ✅ | `product_list.html` - Modern UI |
| 5 | Filter "bisa dijual" | ✅ | `views.py` - 16 produk displayed |
| 6 | CRUD Operations | ✅ | Semua views tersedia |
| 7 | Form Validation | ✅ | `forms.py` - Clean methods |
| 8 | Delete Confirmation | ✅ | `delete_confirm.js` - JS dialog |
| 9 | Django + Serializer | ✅ | Django 5.2 + DRF |
| 10 | PostgreSQL | ✅ | Configured & working |
| 11 | Dokumentasi | ✅ | README + guides |

## 🎨 UI/UX Improvements

**Design Modern:**
- 🎯 Gradient background (purple/indigo)
- 🎯 Professional color scheme
- 🎯 Smooth animations & transitions
- 🎯 Hover effects pada cards
- 🎯 Icons dari FontAwesome
- 🎯 Responsive grid layout
- 🎯 Beautiful empty state
- 🎯 Shadow effects profesional

**User Experience:**
- ✅ Fast load time
- ✅ Smooth navigation
- ✅ Clear visual hierarchy
- ✅ Intuitive CRUD flow
- ✅ Form validation feedback
- ✅ Delete confirmation alerts

## 📁 File Structure

```
fastprint_project/
├── fastprint_project/
│   ├── settings.py           # Django config + PostgreSQL
│   ├── urls.py               # URL routing
│   ├── wsgi.py
│   └── asgi.py
│
├── products/
│   ├── models.py             # Kategori, Status, Product
│   ├── views.py              # CRUD views + API views
│   ├── forms.py              # ProductForm dengan validasi
│   ├── services.py           # FastPrintAPIService
│   ├── serializers.py        # DRF Serializers
│   ├── urls.py               # App routing
│   ├── admin.py              # Admin configuration
│   │
│   ├── templates/products/
│   │   ├── base.html         # ✨ Professional base template
│   │   ├── product_list.html # ✨ Modern product grid
│   │   ├── product_form.html # ✨ Styled form
│   │   ├── product_detail.html
│   │   ├── product_create.html
│   │   └── product_delete.html
│   │
│   └── static/
│       ├── css/style.css
│       └── js/delete_confirm.js
│
├── docs/
│   └── PROJECT_COMPLETION_REPORT.md
│
├── README.md              # ← You are here
├── QUICK_REFERENCE.md
├── SETUP_GUIDE.md
├── DOKUMENTASI_TEKNIS.md
├── requirements.txt
└── manage.py
```

## 🔑 API Configuration

### Endpoint
```
POST https://recruitment.fastprint.co.id/tes/api_tes_programmer
```

### Auto-Generated Credentials
Aplikasi otomatis generate berdasarkan tanggal server:

```python
# services.py - Auto-generate daily
username = "testprogrammerDDMMYYC##"  # e.g., tesprogrammer040226C23
password = MD5("bisacoding-DD-MM-YY")  # e.g., bisacoding-04-02-26
```

### Response Format
```json
{
    "error": 0,
    "version": "220523.0.1",
    "data": [
        {
            "id_produk": "6",
            "nama_produk": "ALCOHOL GEL POLISH CLEANSER",
            "kategori": "L QUEENLY",
            "harga": "12500",
            "status": "bisa dijual"
        }
    ]
}
```

## 🗄️ Database Schema

### Products (Produk)
```sql
- id (PK)
- nama_produk (VARCHAR, Unique)
- harga (INTEGER, > 0)
- kategori_id (FK)
- status_id (FK)
- created_at, updated_at (TIMESTAMP)
```

### Kategori
```sql
- id_kategori (PK)
- nama_kategori (VARCHAR, Unique)
- created_at, updated_at (TIMESTAMP)
```

### Status
```sql
- id_status (PK)
- nama_status (VARCHAR, Unique)
- created_at, updated_at (TIMESTAMP)
```

## 🧪 Testing & Verification

### Run Verification
```bash
python verify_requirements.py   # Verify all requirements
python final_test.py           # Integration testing
python sync_api.py             # Sync API data
```

## 📚 Documentation Files

- **README.md** (you are here) - Overview & quick start
- **QUICK_REFERENCE.md** - Command & endpoint reference
- **SETUP_GUIDE.md** - Detailed setup instructions
- **DOKUMENTASI_TEKNIS.md** - Technical documentation
- **docs/PROJECT_COMPLETION_REPORT.md** - Full completion report

## 🚨 Troubleshooting

### Products tidak muncul
```bash
python sync_api.py
# atau kunjungi http://localhost:8000/fetch-api/
```

### API authentication gagal
- Check response header: `X-Credentials-Username`
- Update username format di `services.py` jika berubah
- Password auto-generate sesuai tanggal

### Database connection error
- Pastikan PostgreSQL running
- Verify credentials di `settings.py`
- Pastikan database `fastprint_db` exists

## 📊 Project Status

- ✅ **Completion**: 100% (All 11 requirements met)
- ✅ **Testing**: All tests passed
- ✅ **Documentation**: Complete
- ✅ **UI/UX**: Professional modern design
- ✅ **Ready for Submission**: YES

## 💼 Submission Checklist

- ✅ Push to GitHub
- ✅ All features working
- ✅ Database populated (30 products)
- ✅ CRUD operations verified
- ✅ Form validation working
- ✅ Delete confirmation working
- ✅ Professional design implemented
- ✅ Documentation complete

## 📧 Contact & Submission

Submit ke:
- **prog3.fastprintsby@gmail.com**
- **adm.hrdfastprint@gmail.com**

Subject: `Test Programmer - [Nama Anda]`

Body:
```
Repository: [GitHub link]
Framework: Django 5.2 + DRF
Database: PostgreSQL
Design: Modern Professional
Status: Ready for Production
```

---

**Last Updated**: February 4, 2026  
**Status**: ✅ Production Ready  
**Framework**: Django 5.2.10 + DRF  
**Database**: PostgreSQL  
**Design**: Professional Modern Gradient
- Custom actions: `/api/products/fetch_from_api/`

### 7. **templates/**
Template HTML untuk UI:
- **base.html**: Base template dengan navbar dan footer
- **product_list.html**: Daftar produk dengan filter dan pagination
- **product_form.html**: Form create/update
- **product_detail.html**: Detail produk
- **product_confirm_delete.html**: Konfirmasi delete
- **fetch_api.html**: Interface sinkronisasi API

### 8. **settings.py**
Django settings configuration:
- Database: PostgreSQL
- Installed apps: Django + DRF + products
- Templates directory configuration
- REST Framework settings
- Timezone: Asia/Jakarta

### 9. **admin.py**
Django admin configuration:
- Admin panels untuk Kategori, Status, Product
- List display, search, filter configuration

---

## 🚀 Installation & Setup

### 1. Install Dependencies
```bash
pip install django djangorestframework psycopg2-binary requests
```

### 2. Create PostgreSQL Database
```bash
createdb fastprint_db
```

Update credentials di `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'fastprint_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 3. Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser (untuk admin)
```bash
python manage.py createsuperuser
```

### 5. Run Development Server
```bash
python manage.py runserver
```

Server akan berjalan di: `http://127.0.0.1:8000/`

---

## 📊 Database Schema

### Tabel: products_kategori
| Field | Type | Description |
|-------|------|-------------|
| id_kategori | AutoField | Primary Key |
| nama_kategori | CharField | Nama kategori (unique) |
| created_at | DateTimeField | Timestamp dibuat |
| updated_at | DateTimeField | Timestamp diperbarui |

### Tabel: products_status
| Field | Type | Description |
|-------|------|-------------|
| id_status | AutoField | Primary Key |
| nama_status | CharField | Nama status (unique) |
| created_at | DateTimeField | Timestamp dibuat |
| updated_at | DateTimeField | Timestamp diperbarui |

### Tabel: products_product
| Field | Type | Description |
|-------|------|-------------|
| id_produk | AutoField | Primary Key |
| nama_produk | CharField | Nama produk (required) |
| harga | DecimalField | Harga produk (numeric) |
| kategori | ForeignKey | Reference ke Kategori |
| status | ForeignKey | Reference ke Status |
| deskripsi | TextField | Deskripsi (optional) |
| created_at | DateTimeField | Timestamp dibuat |
| updated_at | DateTimeField | Timestamp diperbarui |

---

## 🔗 API Endpoints

### REST API Endpoints

#### Products
- `GET /api/products/` - Daftar semua produk (status "bisa dijual")
- `POST /api/products/` - Create produk baru
- `GET /api/products/<id>/` - Detail produk
- `PUT /api/products/<id>/` - Update produk
- `DELETE /api/products/<id>/` - Delete produk
- `GET /api/products/fetch_from_api/?username=user` - Sinkronisasi dari API eksternal

#### Kategoris
- `GET /api/kategoris/` - Daftar semua kategori

#### Statuses
- `GET /api/statuses/` - Daftar semua status

### Web Pages

#### Product Management
- `GET /` - Daftar produk (dengan filter & pagination)
- `GET /products/create/` - Form tambah produk
- `POST /products/create/` - Submit form tambah produk
- `GET /products/<id>/` - Detail produk
- `GET /products/<id>/update/` - Form edit produk
- `POST /products/<id>/update/` - Submit form edit produk
- `GET /products/<id>/delete/` - Konfirmasi hapus produk
- `POST /products/<id>/delete/` - Submit hapus produk

#### API Sync
- `GET /fetch-api/` - Interface sinkronisasi API
- `POST /fetch-api/` - Trigger sinkronisasi

---

## ✅ Features & Validasi

### Filter & Pagination
- ✅ Filter produk by search keyword (nama_produk)
- ✅ Filter produk by kategori
- ✅ Pagination (10 items per page)
- ✅ Hanya display produk dengan status "bisa dijual"

### Validasi Form
- ✅ nama_produk: required, min 3 karakter, max 255 karakter
- ✅ harga: required, numeric, positif (> 0)
- ✅ kategori: required
- ✅ status: required
- ✅ Validation error messages user-friendly

### Confirmation Alert
- ✅ JavaScript `confirm()` untuk delete action
- ✅ Halaman konfirmasi delete yang detail
- ✅ Tindakan tidak dapat dibatalkan

### API Eksternal
- ✅ Fetch data dari: https://recruitment.fastprint.co.id/tes/api_tes_programmer
- ✅ Basic Auth dengan MD5 password
- ✅ Password format: `bisacoding-DD-MM-YY`
- ✅ Parse response dan save ke database
- ✅ Error handling yang komprehensif

---

## 🔐 Authentication & Security

### API Authentication
- Basic Auth header format: `Authorization: Basic <base64_encoded_credentials>`
- Username bisa diubah dinamis
- Password MD5 di-generate otomatis per hari

### Django Security
- CSRF protection di semua POST forms
- SQL injection protection (ORM)
- XSS protection (template escaping)

---

## 📝 Usage Example

### 1. Sinkronisasi Data dari API Eksternal
```bash
# Akses web interface
http://localhost:8000/fetch-api/

# Atau via API
GET /api/products/fetch_from_api/?username=user
```

### 2. Create Produk
```python
# Via web form
POST /products/create/
Form fields: nama_produk, harga, kategori, status, deskripsi

# Via REST API
POST /api/products/
JSON: {
    "nama_produk": "Kertas A4",
    "harga": 50000,
    "kategori": 1,
    "status": 1,
    "deskripsi": "Kertas A4 premium"
}
```

### 3. Update Produk
```python
# Via web form
POST /products/{id}/update/

# Via REST API
PUT /api/products/{id}/
```

### 4. Delete Produk
```python
# Via web (dengan confirmation)
GET /products/{id}/delete/
POST /products/{id}/delete/

# Via REST API
DELETE /api/products/{id}/
```

---

## 🧪 Testing

### Run Unit Tests
```bash
python manage.py test
```

### Test Coverage
- Model tests: Creation, string representation, relationships
- View tests: HTTP status codes, template rendering
- Form tests: Validation rules

---

## 📦 Dependencies

```
Django==5.2.10
djangorestframework==3.14.0
psycopg2-binary==2.9.9
requests==2.31.0
```

Install all:
```bash
pip install -r requirements.txt
```

---

## 🎯 Next Steps / Improvements

- [ ] Add image/thumbnail field untuk produk
- [ ] Implement caching untuk API response
- [ ] Add email notification untuk CRUD actions
- [ ] Export data to CSV/Excel
- [ ] Advanced filtering dan sorting
- [ ] User authentication & permissions
- [ ] Product reviews/ratings
- [ ] Inventory management
- [ ] QR code generation untuk produk

---

## 👨‍💻 Author & License

**Fast Print Indonesia - Technical Test for Junior Programmer**

Created with ❤️ using Django & DRF

---

## 📞 Support

Untuk pertanyaan atau issue, silakan contact admin.

Happy coding! 🚀
