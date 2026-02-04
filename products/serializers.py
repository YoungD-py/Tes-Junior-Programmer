from rest_framework import serializers
from .models import Product, Kategori, Status


class KategoriSerializer(serializers.ModelSerializer):
    """
    Serializer untuk model Kategori.
    Mengkonversi data Kategori menjadi JSON dan sebaliknya.
    """
    class Meta:
        model = Kategori
        fields = ['id_kategori', 'nama_kategori', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class StatusSerializer(serializers.ModelSerializer):
    """
    Serializer untuk model Status.
    Mengkonversi data Status menjadi JSON dan sebaliknya.
    """
    class Meta:
        model = Status
        fields = ['id_status', 'nama_status', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer untuk model Product.
    Mengkonversi data Product menjadi JSON dan sebaliknya.
    
    Includes:
    - Nested serializers untuk kategori dan status
    - Validasi untuk nama_produk (required) dan harga (numeric)
    """
    kategori_detail = KategoriSerializer(source='kategori', read_only=True)
    status_detail = StatusSerializer(source='status', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id_produk', 
            'nama_produk', 
            'harga', 
            'kategori',
            'kategori_detail',
            'status',
            'status_detail',
            'deskripsi',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_nama_produk(self, value):
        """Validasi bahwa nama_produk tidak kosong."""
        if not value or not value.strip():
            raise serializers.ValidationError("Nama produk tidak boleh kosong.")
        return value

    def validate_harga(self, value):
        """Validasi bahwa harga adalah angka positif."""
        if value < 0:
            raise serializers.ValidationError("Harga tidak boleh negatif.")
        return value


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer khusus untuk Create dan Update product.
    Validasi lebih ketat untuk form submission.
    """
    class Meta:
        model = Product
        fields = [
            'nama_produk',
            'harga',
            'kategori',
            'status',
            'deskripsi'
        ]

    def validate_nama_produk(self, value):
        """Validasi bahwa nama_produk tidak kosong."""
        if not value or not value.strip():
            raise serializers.ValidationError("Nama produk harus diisi.")
        if len(value) < 3:
            raise serializers.ValidationError("Nama produk minimal 3 karakter.")
        return value

    def validate_harga(self, value):
        """Validasi bahwa harga adalah angka positif."""
        if not isinstance(value, (int, float)):
            raise serializers.ValidationError("Harga harus berupa angka.")
        if value <= 0:
            raise serializers.ValidationError("Harga harus lebih besar dari 0.")
        return value
