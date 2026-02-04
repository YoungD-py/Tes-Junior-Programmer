#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fastprint_project.settings')
django.setup()

from django.contrib.auth.models import User

users = User.objects.all()
print(f"Total users: {users.count()}")
for user in users:
    print(f"  - {user.username} (admin: {user.is_staff})")

# Create superuser if not exists
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@fastprint.local', 'admin123')
    print("\n✅ Superuser 'admin' created with password 'admin123'")
else:
    print("\n✅ Superuser 'admin' already exists")
