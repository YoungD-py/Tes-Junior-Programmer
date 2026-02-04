# 🚀 SETUP & INSTALLATION GUIDE

## 📋 Requirements

- Python 3.8 atau lebih tinggi
- PostgreSQL 12 atau lebih tinggi
- pip (Python package manager)
- Virtual Environment (recommended)

---

## ⚡ Quick Setup (Windows)

### Step 1: Buat Virtual Environment

```bash
cd d:\fastPrint\fastprint_project
python -m venv venv
venv\Scripts\activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Setup PostgreSQL Database

**Pastikan PostgreSQL sudah terinstall dan running!**

```bash
# Buka PostgreSQL command line
psql -U postgres

# Buat database
CREATE DATABASE fastprint_db;

# Exit
\q
```

### Step 4: Update Database Credentials

Edit file: `fastprint_project/settings.py`

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'fastprint_db',
        'USER': 'postgres',          # Your PostgreSQL username
        'PASSWORD': 'your_password',  # Your PostgreSQL password
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Step 5: Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

Masukkan:
- Username: `admin`
- Email: `admin@example.com`
- Password: `your_secure_password`

### Step 7: Run Development Server

```bash
python manage.py runserver
```

Server akan berjalan di: **http://127.0.0.1:8000/**

---

## 🌐 Akses Aplikasi

### Web Interface
- **Products List**: http://localhost:8000/
- **Add Product**: http://localhost:8000/products/create/
- **API Sync**: http://localhost:8000/fetch-api/

### Admin Panel
- **Admin Dashboard**: http://localhost:8000/admin/
- Username: `admin`
- Password: (sesuai yang Anda buat)

### API Endpoints (REST Framework)
- **Products API**: http://localhost:8000/api/products/
- **Categories API**: http://localhost:8000/api/kategoris/
- **Status API**: http://localhost:8000/api/statuses/

---

## 🗂️ Folder Structure

Setelah setup, struktur folder akan seperti ini:

```
fastprint_project/
├── venv/                      # Virtual environment (dibuat otomatis)
├── products/                  # Main Django app
│   ├── migrations/            # Database migrations
│   ├── templates/             # HTML templates
│   ├── static/                # CSS, JS files
│   ├── models.py              # Database models
│   ├── views.py               # Views/Controllers
│   ├── urls.py                # URL routing
│   ├── serializers.py         # DRF serializers
│   └── ...
├── fastprint_project/         # Project settings
│   ├── settings.py            # ⭐ UPDATE DATABASE CREDENTIALS HERE
│   ├── urls.py
│   └── ...
├── static/                    # Static files (CSS, JS)
├── templates/                 # Global templates
├── manage.py                  # Django CLI
├── requirements.txt           # Dependencies list
└── README.md                  # Project documentation
```

---

## 🔧 Configuration Changes

### File: `fastprint_project/settings.py`

#### 1. Database Configuration

```python
# BEFORE (SQLite - default)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# AFTER (PostgreSQL)
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

#### 2. Installed Apps (sudah diupdate)

```python
INSTALLED_APPS = [
    ...
    'rest_framework',    # ✓ Added
    'products',          # ✓ Added
]
```

#### 3. Templates Directory (sudah diupdate)

```python
TEMPLATES = [
    {
        'DIRS': [BASE_DIR / 'templates'],  # ✓ Updated
        ...
    }
]
```

---

## 📦 Create Initial Data

### Menggunakan Django Shell

```bash
python manage.py shell
```

```python
from products.models import Kategori, Status

# Create Kategoris
kategori1 = Kategori.objects.create(nama_kategori="Kertas")
kategori2 = Kategori.objects.create(nama_kategori="Tinta")
kategori3 = Kategori.objects.create(nama_kategori="Toner")

# Create Statuses
status1 = Status.objects.create(nama_status="bisa dijual")
status2 = Status.objects.create(nama_status="tidak tersedia")

print("✓ Initial data created successfully!")
exit()
```

### Atau Menggunakan Admin Panel

1. Buka: http://localhost:8000/admin/
2. Login dengan superuser credentials
3. Click "Tambah" di Kategori dan Status
4. Isi data yang diperlukan

---

## 🧪 Testing

### Run All Tests

```bash
python manage.py test
```

### Run Specific App Tests

```bash
python manage.py test products
```

### Run Specific Test Class

```bash
python manage.py test products.tests.ProductModelTest
```

### Run with Verbose Output

```bash
python manage.py test -v 2
```

---

## 📝 Sample Data

### Sample API Sync

Buka: http://localhost:8000/fetch-api/

1. Enter username: `user` (atau custom)
2. Click "Sinkronisasi Sekarang"
3. Data dari API akan disimpan ke database

### Manual Product Creation

1. Go to: http://localhost:8000/products/create/
2. Fill form:
   - Nama Produk: "Kertas A4 Premium"
   - Harga: 50000
   - Kategori: "Kertas"
   - Status: "bisa dijual"
   - Deskripsi: (optional)
3. Click "Tambah Produk"

---

## 🐛 Troubleshooting

### Error: "No module named 'psycopg2'"

**Solution:**
```bash
pip install psycopg2-binary
```

### Error: "Can't connect to PostgreSQL"

**Check:**
1. PostgreSQL service running?
2. Username & password correct?
3. Database exists?
4. Port 5432 open?

```bash
# Test connection
psql -U postgres -h localhost -d fastprint_db
```

### Error: "Module not found"

**Solution:**
```bash
# Ensure virtual environment is activated
# Windows:
venv\Scripts\activate

# Then reinstall:
pip install -r requirements.txt
```

### Error: "No migrations found"

**Solution:**
```bash
python manage.py makemigrations products
python manage.py migrate
```

### Migrations not applied

**Solution:**
```bash
python manage.py migrate --run-syncdb
python manage.py migrate
```

---

## 🚀 Run Server

### Development Server

```bash
python manage.py runserver
```

Output:
```
Starting development server at http://127.0.0.1:8000/
Press CTRL+C to quit.
```

### Custom Port

```bash
python manage.py runserver 8080
```

### All Network Interfaces

```bash
python manage.py runserver 0.0.0.0:8000
```

---

## 📊 Database Management

### Make Migrations

```bash
# Auto-detect changes
python manage.py makemigrations

# Specific app
python manage.py makemigrations products
```

### Apply Migrations

```bash
python manage.py migrate
```

### Show Migration Status

```bash
python manage.py showmigrations
```

### Rollback Migration

```bash
# Show available migrations
python manage.py showmigrations products

# Rollback to specific migration
python manage.py migrate products 0001_initial
```

---

## 💻 Development Commands

### Django Shell (Interactive Python)

```bash
python manage.py shell
```

### Create Superuser

```bash
python manage.py createsuperuser
```

### Change Superuser Password

```bash
python manage.py changepassword admin
```

### Dump Data (Backup)

```bash
python manage.py dumpdata > backup.json
```

### Load Data (Restore)

```bash
python manage.py loaddata backup.json
```

### Clear Database

```bash
python manage.py flush --no-input
```

---

## 📦 Requirements Versions

```
Django==5.2.10
djangorestframework==3.14.0
psycopg2-binary==2.9.9
requests==2.31.0
```

### Update Requirements

```bash
# Update specific package
pip install --upgrade django

# Update all packages
pip install --upgrade -r requirements.txt

# Save current dependencies
pip freeze > requirements.txt
```

---

## ✅ Verify Installation

### Check Django

```bash
python -c "import django; print(f'Django {django.VERSION}')"
```

### Check Database Connection

```bash
python manage.py dbshell
```

### Check All Installed Apps

```bash
python manage.py check
```

### Run Development Server Check

```bash
python manage.py check --deploy
```

---

## 🎯 Next Steps After Setup

1. ✓ Test product list page
2. ✓ Create sample products
3. ✓ Test API endpoints using Postman or cURL
4. ✓ Test API synchronization feature
5. ✓ Test delete confirmation alert
6. ✓ Run tests to ensure everything works

---

## 📚 Useful Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Bootstrap 5 Docs](https://getbootstrap.com/docs/5.0/)

---

## 🆘 Need Help?

1. Check DOKUMENTASI_TEKNIS.md for technical details
2. Check README.md for project overview
3. Review code comments for explanations
4. Check Django/DRF official documentation

Happy coding! 🚀
