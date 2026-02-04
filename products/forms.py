"""
Forms untuk Product Create dan Update.
Includes custom validasi rules.
"""

from django import forms
from .models import Product, Kategori, Status


class ProductForm(forms.ModelForm):
    """
    Form untuk Create dan Update Product.
    
    Validasi:
    - nama_produk: required, min 3 karakter
    - harga: required, numeric, positif
    - kategori: required
    - status: required
    """
    
    class Meta:
        model = Product
        fields = ['nama_produk', 'harga', 'kategori', 'status', 'deskripsi']
        widgets = {
            'nama_produk': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan nama produk',
                'required': True,
            }),
            'harga': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan harga (angka)',
                'min': '0',
                'step': '0.01',
                'required': True,
            }),
            'kategori': forms.Select(attrs={
                'class': 'form-control',
                'required': True,
            }),
            'status': forms.Select(attrs={
                'class': 'form-control',
                'required': True,
            }),
            'deskripsi': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Deskripsi produk (opsional)',
                'rows': 4,
            }),
        }
    
    def clean_nama_produk(self):
        """Validasi nama_produk."""
        nama_produk = self.cleaned_data.get('nama_produk', '').strip()
        
        if not nama_produk:
            raise forms.ValidationError('Nama produk tidak boleh kosong.')
        
        if len(nama_produk) < 3:
            raise forms.ValidationError('Nama produk minimal 3 karakter.')
        
        if len(nama_produk) > 255:
            raise forms.ValidationError('Nama produk maksimal 255 karakter.')
        
        return nama_produk
    
    def clean_harga(self):
        """Validasi harga."""
        harga = self.cleaned_data.get('harga')
        
        if harga is None:
            raise forms.ValidationError('Harga tidak boleh kosong.')
        
        try:
            harga_float = float(harga)
        except (ValueError, TypeError):
            raise forms.ValidationError('Harga harus berupa angka.')
        
        if harga_float <= 0:
            raise forms.ValidationError('Harga harus lebih besar dari 0.')
        
        if harga_float > 999999999999:
            raise forms.ValidationError('Harga terlalu besar.')
        
        return harga
    
    def clean_kategori(self):
        """Validasi kategori tidak boleh kosong."""
        kategori = self.cleaned_data.get('kategori')
        
        if not kategori:
            raise forms.ValidationError('Kategori harus dipilih.')
        
        return kategori
    
    def clean_status(self):
        """Validasi status tidak boleh kosong."""
        status = self.cleaned_data.get('status')
        
        if not status:
            raise forms.ValidationError('Status harus dipilih.')
        
        return status
