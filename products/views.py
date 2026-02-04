"""
Views untuk Product CRUD operations.
Menggunakan class-based views dan function-based views.
Display hanya produk dengan status "bisa dijual".
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import logging

from .models import Product, Kategori, Status
from .serializers import ProductSerializer, ProductCreateUpdateSerializer, KategoriSerializer, StatusSerializer
from .services import FastPrintAPIService
from .forms import ProductForm

logger = logging.getLogger(__name__)


# ============================================================================
# API Views (REST Framework)
# ============================================================================

class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet untuk REST API endpoint.
    Menyediakan list, create, retrieve, update, delete operations.
    """
    permission_classes = [AllowAny]
    queryset = Product.objects.all().select_related('kategori', 'status')
    serializer_class = ProductSerializer
    pagination_class = None

    def get_queryset(self):
        """
        Filter hanya produk dengan status "bisa dijual".
        Support filtering by kategori dan status.
        """
        queryset = super().get_queryset()
        
        # Filter by status "bisa dijual"
        queryset = queryset.filter(status__nama_status='bisa dijual')
        
        # Optional filters
        kategori = self.request.query_params.get('kategori')
        if kategori:
            queryset = queryset.filter(kategori__id_kategori=kategori)
        
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(nama_produk__icontains=search)
        
        return queryset

    def get_serializer_class(self):
        """Gunakan ProductCreateUpdateSerializer untuk create/update operations."""
        if self.action in ['create', 'update', 'partial_update']:
            return ProductCreateUpdateSerializer
        return ProductSerializer

    @action(detail=False, methods=['get'])
    def fetch_from_api(self, request):
        """
        Endpoint custom untuk fetch data dari API eksternal.
        
        GET /api/products/fetch_from_api/?username=user
        """
        try:
            username = request.query_params.get('username', 'user')
            
            # Fetch data dari API eksternal
            api_response = FastPrintAPIService.fetch_products(username)
            
            # Parse data produk
            products_data = FastPrintAPIService.parse_product_data(api_response)
            
            # Save ke database
            saved_count = 0
            for prod_data in products_data:
                # Get atau create kategori
                kategori, _ = Kategori.objects.get_or_create(
                    nama_kategori=prod_data['kategori']
                )
                
                # Get atau create status
                status_obj, _ = Status.objects.get_or_create(
                    nama_status=prod_data['status']
                )
                
                # Create atau update produk
                Product.objects.update_or_create(
                    nama_produk=prod_data['nama_produk'],
                    defaults={
                        'harga': prod_data['harga'],
                        'kategori': kategori,
                        'status': status_obj,
                    }
                )
                saved_count += 1
            
            return Response({
                'success': True,
                'message': f'Berhasil menyimpan {saved_count} produk',
                'count': saved_count,
                'api_response': api_response
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"Error fetching products from API: {str(e)}")
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def by_kategori(self, request):
        """
        Endpoint untuk get produk berdasarkan kategori.
        
        GET /api/products/by_kategori/?kategori_id=1
        """
        kategori_id = request.query_params.get('kategori_id')
        if not kategori_id:
            return Response(
                {'error': 'kategori_id parameter required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.get_queryset().filter(kategori__id_kategori=kategori_id)
        serializer = self.get_serializer(queryset, many=True)
        
        return Response({
            'count': len(serializer.data),
            'results': serializer.data
        }, status=status.HTTP_200_OK)


class KategoriViewSet(viewsets.ReadOnlyModelViewSet):
    """ReadOnly ViewSet untuk Kategori."""
    queryset = Kategori.objects.all()
    serializer_class = KategoriSerializer
    permission_classes = [AllowAny]
    pagination_class = None


class StatusViewSet(viewsets.ReadOnlyModelViewSet):
    """ReadOnly ViewSet untuk Status."""
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [AllowAny]
    pagination_class = None


# ============================================================================
# Web Views (Template Based)
# ============================================================================

def product_list(request):
    """
    View untuk display daftar produk dengan status "bisa dijual".
    Support pagination dan filtering.
    
    Template: products/product_list.html
    """
    
    # Filter hanya produk dengan status "bisa dijual"
    products = Product.objects.filter(
        status__nama_status='bisa dijual'
    ).select_related('kategori', 'status')
    
    # Filter by search
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(nama_produk__icontains=search_query)
    
    # Filter by kategori
    kategori_filter = request.GET.get('kategori')
    if kategori_filter:
        products = products.filter(kategori__id_kategori=kategori_filter)
    
    # Pagination
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all kategoris untuk dropdown filter
    kategoris = Kategori.objects.all()
    
    context = {
        'page_obj': page_obj,
        'products': page_obj.object_list,
        'kategoris': kategoris,
        'search_query': search_query,
        'kategori_filter': kategori_filter,
    }
    
    return render(request, 'products/product_list.html', context)


def product_detail(request, pk):
    """
    View untuk detail produk.
    
    Template: products/product_detail.html
    """
    product = get_object_or_404(Product, id_produk=pk)
    
    context = {
        'product': product,
    }
    
    return render(request, 'products/product_detail.html', context)


def product_create(request):
    """
    View untuk create produk baru.
    
    Template: products/product_form.html
    """
    if request.method == 'POST':
        form = ProductForm(request.POST)
        
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Produk "{product.nama_produk}" berhasil ditambahkan.')
            return redirect('product_list')
        else:
            # Validasi error
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ProductForm()
    
    context = {
        'form': form,
        'title': 'Tambah Produk Baru',
        'button_text': 'Tambah Produk',
    }
    
    return render(request, 'products/product_form.html', context)


def product_update(request, pk):
    """
    View untuk update produk.
    
    Template: products/product_form.html
    """
    product = get_object_or_404(Product, id_produk=pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Produk "{product.nama_produk}" berhasil diperbarui.')
            return redirect('product_detail', pk=product.id_produk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ProductForm(instance=product)
    
    context = {
        'form': form,
        'product': product,
        'title': f'Edit Produk: {product.nama_produk}',
        'button_text': 'Update Produk',
    }
    
    return render(request, 'products/product_form.html', context)


def product_delete(request, pk):
    """
    View untuk delete produk.
    Menampilkan halaman konfirmasi delete.
    
    Template: products/product_confirm_delete.html
    """
    product = get_object_or_404(Product, id_produk=pk)
    
    if request.method == 'POST':
        product_name = product.nama_produk
        product.delete()
        messages.success(request, f'Produk "{product_name}" berhasil dihapus.')
        return redirect('product_list')
    
    context = {
        'product': product,
    }
    
    return render(request, 'products/product_confirm_delete.html', context)


def fetch_api_data(request):
    """
    View untuk trigger fetch data dari API eksternal.
    
    Template: products/fetch_api.html
    """
    if request.method == 'POST':
        try:
            username = request.POST.get('username', None)
            
            # Fetch data dari API (akan generate username otomatis jika tidak diberikan)
            api_response = FastPrintAPIService.fetch_products(username)
            products_data = FastPrintAPIService.parse_product_data(api_response)
            
            # Save ke database
            saved_count = 0
            for prod_data in products_data:
                kategori, _ = Kategori.objects.get_or_create(
                    nama_kategori=prod_data['kategori']
                )
                status_obj, _ = Status.objects.get_or_create(
                    nama_status=prod_data['status']
                )
                Product.objects.update_or_create(
                    nama_produk=prod_data['nama_produk'],
                    defaults={
                        'harga': prod_data['harga'],
                        'kategori': kategori,
                        'status': status_obj,
                    }
                )
                saved_count += 1
            
            messages.success(request, f'Berhasil menyimpan {saved_count} produk dari API.')
            return redirect('product_list')
        
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    context = {}
    return render(request, 'products/fetch_api.html', context)
