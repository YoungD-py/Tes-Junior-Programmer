"""
Django Admin Configuration untuk app products.
"""

from django.contrib import admin
from .models import Product, Kategori, Status


@admin.register(Kategori)
class KategoriAdmin(admin.ModelAdmin):
    """Admin untuk model Kategori."""
    list_display = ['id_kategori', 'nama_kategori', 'created_at', 'updated_at']
    search_fields = ['nama_kategori']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['nama_kategori']


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    """Admin untuk model Status."""
    list_display = ['id_status', 'nama_status', 'created_at', 'updated_at']
    search_fields = ['nama_status']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['nama_status']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin untuk model Product."""
    list_display = ['id_produk', 'nama_produk', 'harga', 'kategori', 'status', 'created_at']
    list_filter = ['kategori', 'status', 'created_at']
    search_fields = ['nama_produk', 'id_produk']
    readonly_fields = ['id_produk', 'created_at', 'updated_at']
    fieldsets = (
        ('Informasi Produk', {
            'fields': ('id_produk', 'nama_produk', 'harga', 'deskripsi')
        }),
        ('Kategori & Status', {
            'fields': ('kategori', 'status')
        }),
        ('Timestamp', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    ordering = ['-created_at']
