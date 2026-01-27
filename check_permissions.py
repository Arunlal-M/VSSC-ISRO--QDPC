#!/usr/bin/env python
"""
Script to check user permissions for debugging product batch edit access
Run this with: python manage.py shell < check_permissions.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qdpc.settings')
django.setup()

from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

def check_user_permissions(username):
    """Check permissions for a specific user"""
    try:
        user = User.objects.get(username=username)
        print(f"\n=== User: {username} ===")
        print(f"is_superuser: {user.is_superuser}")
        print(f"is_staff: {user.is_staff}")
        print(f"is_active: {user.is_active}")
        
        # Check groups
        groups = user.groups.all()
        print(f"Groups: {[g.name for g in groups]}")
        
        # Check custom role if exists
        if hasattr(user, 'role') and user.role:
            print(f"Custom Role: {user.role.name}")
        
        # Check permissions
        permissions = user.user_permissions.all()
        print(f"Direct Permissions: {[f'{p.content_type.app_label}.{p.codename}' for p in permissions]}")
        
        # Check group permissions
        group_permissions = set()
        for group in groups:
            for perm in group.permissions.all():
                group_permissions.add(f'{perm.content_type.app_label}.{perm.codename}')
        
        print(f"Group Permissions: {list(group_permissions)}")
        
        # Check specific permissions we care about
        specific_perms = [
            'qdpc_core_models.change_productbatch',
            'product.change_productbatch',
            'qdpc_core_models.change_product',
            'product.change_product'
        ]
        
        print(f"\nSpecific Permission Checks:")
        for perm in specific_perms:
            has_perm = user.has_perm(perm)
            print(f"  {perm}: {has_perm}")
        
        # Check if user would have edit access
        has_custom_role = (hasattr(user, 'role') and user.role and 
                          str(user.role.name).upper() in {"SUPER ADMIN", "MASTER ADMIN", "ADMIN"})
        has_admin_group = user.groups.filter(name__in=['SUPER ADMIN', 'MASTER ADMIN', 'ADMIN']).exists()
        has_edit_permission = (user.has_perm('qdpc_core_models.change_productbatch') or 
                              user.has_perm('product.change_productbatch'))
        has_product_edit_permission = (user.has_perm('qdpc_core_models.change_product') or 
                                     user.has_perm('product.change_product'))
        
        final_permission = user.is_superuser or has_custom_role or has_admin_group or has_edit_permission or has_product_edit_permission
        
        print(f"\nFinal Edit Permission: {final_permission}")
        print(f"  - is_superuser: {user.is_superuser}")
        print(f"  - has_custom_role: {has_custom_role}")
        print(f"  - has_admin_group: {has_admin_group}")
        print(f"  - has_edit_permission: {has_edit_permission}")
        print(f"  - has_product_edit_permission: {has_product_edit_permission}")
        
    except User.DoesNotExist:
        print(f"User '{username}' not found")

def list_all_users():
    """List all users in the system"""
    users = User.objects.all()
    print(f"\n=== All Users ===")
    for user in users:
        print(f"  {user.username} (superuser: {user.is_superuser}, active: {user.is_active})")

def list_all_groups():
    """List all groups in the system"""
    from django.contrib.auth.models import Group
    groups = Group.objects.all()
    print(f"\n=== All Groups ===")
    for group in groups:
        print(f"  {group.name}")

if __name__ == "__main__":
    print("=== Django Permission Checker ===")
    
    # List all users and groups
    list_all_users()
    list_all_groups()
    
    # Check specific users (replace with actual usernames)
    print("\n=== Checking Specific Users ===")
    
    # Check superuser if exists
    superusers = User.objects.filter(is_superuser=True)
    if superusers.exists():
        check_user_permissions(superusers.first().username)
    
    # Check first few regular users
    regular_users = User.objects.filter(is_superuser=False)[:3]
    for user in regular_users:
        check_user_permissions(user.username)
    
    print("\n=== Done ===")
