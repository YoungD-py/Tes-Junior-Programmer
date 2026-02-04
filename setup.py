#!/usr/bin/env python
"""
Setup Script untuk Fast Print Django Application
Jalankan script ini untuk melakukan initial setup setelah clone project
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Jalankan command dan tampilkan status"""
    print(f"\n{'='*60}")
    print(f"▶ {description}")
    print(f"{'='*60}")
    print(f"Command: {command}\n")
    
    result = subprocess.run(command, shell=True)
    
    if result.returncode != 0:
        print(f"\n✗ Error saat: {description}")
        return False
    
    print(f"✓ {description} - SUCCESS")
    return True

def main():
    """Main setup function"""
    
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║           Fast Print Django App - Setup Script               ║
    ║                    Technical Test v1.0                       ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    
    # Check Python version
    print(f"Python Version: {sys.version}")
    if sys.version_info < (3, 8):
        print("✗ Python 3.8+ required!")
        sys.exit(1)
    
    # 1. Install dependencies
    if not run_command(
        "pip install -r requirements.txt",
        "1. Installing Python dependencies"
    ):
        sys.exit(1)
    
    # 2. Create migrations
    if not run_command(
        "python manage.py makemigrations",
        "2. Creating database migrations"
    ):
        sys.exit(1)
    
    # 3. Apply migrations
    if not run_command(
        "python manage.py migrate",
        "3. Applying migrations to database"
    ):
        sys.exit(1)
    
    # 4. Collect static files
    if not run_command(
        "python manage.py collectstatic --noinput",
        "4. Collecting static files"
    ):
        print("⚠ Warning: Static files collection failed (may not be critical)")
    
    # 5. Create superuser (optional)
    print(f"\n{'='*60}")
    print("5. Creating superuser")
    print(f"{'='*60}")
    
    create_admin = input("\nDo you want to create a superuser now? (y/n): ").lower()
    if create_admin == 'y':
        subprocess.run("python manage.py createsuperuser")
    
    # 6. Run tests
    print(f"\n{'='*60}")
    print("6. Running tests")
    print(f"{'='*60}")
    
    run_tests = input("\nDo you want to run tests? (y/n): ").lower()
    if run_tests == 'y':
        subprocess.run("python manage.py test")
    
    # Success message
    print(f"""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                    ✓ SETUP COMPLETED!                        ║
    ╚═══════════════════════════════════════════════════════════════╝
    
    Next steps:
    1. Update database credentials in settings.py (if using PostgreSQL)
    2. Run: python manage.py runserver
    3. Access: http://127.0.0.1:8000/
    4. Admin: http://127.0.0.1:8000/admin/
    
    Features:
    ✓ Product CRUD (Create, Read, Update, Delete)
    ✓ Filter by category and search
    ✓ Pagination
    ✓ API synchronization from external API
    ✓ REST API endpoints
    ✓ Validation and error handling
    ✓ Beautiful Bootstrap 5 UI
    
    Documentation:
    - README.md - Project overview
    - DOKUMENTASI_TEKNIS.md - Technical documentation
    
    Happy coding! 🚀
    """)

if __name__ == "__main__":
    main()
