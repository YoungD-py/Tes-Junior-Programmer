/**
 * Delete Confirmation JavaScript
 * Digunakan untuk form delete pada aplikasi Fast Print
 */

/**
 * Fungsi: confirmDelete()
 * Menampilkan JavaScript confirm dialog sebelum delete
 * 
 * @returns {boolean} true jika user klik OK, false jika Cancel
 */
function confirmDelete() {
    const confirmed = confirm(
        '⚠️ Apakah Anda yakin ingin menghapus produk ini?\n\n' +
        'Tindakan ini TIDAK DAPAT DIBATALKAN!\n\n' +
        'Tekan OK untuk menghapus, atau Cancel untuk membatalkan.'
    );
    
    if (confirmed) {
        console.log('User mengklik OK - melanjutkan delete...');
        return true;
    } else {
        console.log('User membatalkan delete');
        return false;
    }
}

/**
 * Fungsi: confirmDeleteWithDetails(productName, productId)
 * Menampilkan confirmation dengan detail produk
 * 
 * @param {string} productName - Nama produk yang akan dihapus
 * @param {number} productId - ID produk
 * @returns {boolean} true jika confirmed, false jika cancel
 */
function confirmDeleteWithDetails(productName, productId) {
    const message = `⚠️ PERHATIAN!\n\n` +
        `Anda akan menghapus produk:\n` +
        `Nama: ${productName}\n` +
        `ID: ${productId}\n\n` +
        `Tindakan ini TIDAK DAPAT DIBATALKAN!\n\n` +
        `Lanjutkan?`;
    
    return confirm(message);
}

/**
 * Fungsi: showDeleteConfirmationModal(productName, productId, callback)
 * Menampilkan Bootstrap modal untuk konfirmasi delete
 * 
 * Requires: Bootstrap 5 atau lebih tinggi
 * 
 * @param {string} productName - Nama produk
 * @param {number} productId - ID produk
 * @param {function} callback - Callback function setelah confirm
 */
function showDeleteConfirmationModal(productName, productId, callback) {
    const modalHtml = `
        <div class="modal fade" id="deleteConfirmModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content border-danger">
                    <div class="modal-header bg-danger text-white">
                        <h5 class="modal-title">⚠️ Konfirmasi Penghapusan</h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <p>Anda akan menghapus produk berikut:</p>
                        <div class="alert alert-warning">
                            <strong>Nama:</strong> ${productName}<br>
                            <strong>ID:</strong> ${productId}
                        </div>
                        <p class="text-danger fw-bold">
                            Tindakan ini TIDAK DAPAT DIBATALKAN!
                        </p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                            Batal
                        </button>
                        <button type="button" class="btn btn-danger" id="confirmDeleteBtn">
                            Hapus Produk
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Insert modal ke page
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    
    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('deleteConfirmModal'));
    modal.show();
    
    // Handle confirm button
    document.getElementById('confirmDeleteBtn').addEventListener('click', function() {
        modal.hide();
        if (callback) {
            callback();
        }
    });
}

/**
 * Fungsi: handleDeleteWithAjax(productId, endpoint)
 * Delete dengan AJAX (non-form submission)
 * 
 * @param {number} productId - ID produk
 * @param {string} endpoint - API endpoint untuk delete (default: '/api/products/{id}/')
 */
async function handleDeleteWithAjax(productId, endpoint = null) {
    if (!endpoint) {
        endpoint = `/api/products/${productId}/`;
    }
    
    if (!confirm('Apakah Anda yakin ingin menghapus produk ini?')) {
        return;
    }
    
    try {
        // Tampilkan loading state
        const loadingMsg = document.createElement('div');
        loadingMsg.className = 'alert alert-info';
        loadingMsg.textContent = '⏳ Sedang menghapus...';
        document.body.appendChild(loadingMsg);
        
        // Send DELETE request
        const response = await fetch(endpoint, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            }
        });
        
        if (response.ok) {
            // Success
            loadingMsg.className = 'alert alert-success';
            loadingMsg.textContent = '✓ Produk berhasil dihapus!';
            
            // Redirect setelah 2 detik
            setTimeout(() => {
                window.location.href = '/';
            }, 2000);
        } else {
            // Error
            loadingMsg.className = 'alert alert-danger';
            loadingMsg.textContent = `✗ Error: ${response.statusText}`;
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Terjadi error saat menghapus: ' + error.message);
    }
}

/**
 * Utility: getCookie(name)
 * Mengambil value dari cookie berdasarkan name
 * 
 * @param {string} name - Cookie name
 * @returns {string} Cookie value atau empty string
 */
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
        return parts.pop().split(';').shift();
    }
    return '';
}

/**
 * Event Listener untuk semua delete buttons
 * Otomatis attach confirmDelete ke semua link dengan class 'delete-btn'
 */
document.addEventListener('DOMContentLoaded', function() {
    // Find all delete buttons
    const deleteButtons = document.querySelectorAll('a.delete-btn, button.delete-btn');
    
    deleteButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            if (!confirmDelete()) {
                e.preventDefault();
                return false;
            }
        });
    });
});

// ============================================================================
// CONTOH PENGGUNAAN DI HTML
// ============================================================================

/*

1. SIMPLE CONFIRM (Inline):
   <a href="/products/1/delete/" onclick="return confirmDelete()">Delete</a>

2. DENGAN DETAILS:
   <a href="/products/1/delete/" 
      onclick="return confirmDeleteWithDetails('Kertas A4', 1)">
      Delete
   </a>

3. DENGAN CLASS SELECTOR:
   <a href="/products/1/delete/" class="delete-btn">Delete</a>
   (akan otomatis attach confirmDelete via event listener)

4. DENGAN MODAL:
   <button type="button" onclick="showDeleteConfirmationModal('Kertas A4', 1, function() {
       fetch('/api/products/1/', {method: 'DELETE'}).then(r => location.href='/');
   })">
       Delete
   </button>

5. DENGAN AJAX:
   <button type="button" onclick="handleDeleteWithAjax(1)">
       Delete with AJAX
   </button>

*/
