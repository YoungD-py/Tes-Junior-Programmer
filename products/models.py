from django.db import models


class Kategori(models.Model):
    """
    Model untuk menyimpan data kategori produk.
    
    Fields:
    - id_kategori: Primary Key
    - nama_kategori: Nama kategori produk
    """
    id_kategori = models.AutoField(primary_key=True)
    nama_kategori = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Kategori"
        ordering = ['nama_kategori']

    def __str__(self):
        return self.nama_kategori


class Status(models.Model):
    """
    Model untuk menyimpan data status produk.
    
    Fields:
    - id_status: Primary Key
    - nama_status: Nama status produk (contoh: "bisa dijual", "tidak tersedia")
    """
    id_status = models.AutoField(primary_key=True)
    nama_status = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Status"
        ordering = ['nama_status']

    def __str__(self):
        return self.nama_status


class Product(models.Model):
    """
    Model untuk menyimpan data produk.
    
    Fields:
    - id_produk: Primary Key
    - nama_produk: Nama produk (required)
    - harga: Harga produk (numeric)
    - kategori: Foreign Key ke model Kategori
    - status: Foreign Key ke model Status
    - deskripsi: Deskripsi produk (optional)
    """
    id_produk = models.AutoField(primary_key=True)
    nama_produk = models.CharField(max_length=255, null=False, blank=False)
    harga = models.DecimalField(max_digits=15, decimal_places=2)
    kategori = models.ForeignKey(Kategori, on_delete=models.PROTECT, related_name='products')
    status = models.ForeignKey(Status, on_delete=models.PROTECT, related_name='products')
    deskripsi = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Produk"
        ordering = ['-created_at']

    def __str__(self):
        return self.nama_produk
