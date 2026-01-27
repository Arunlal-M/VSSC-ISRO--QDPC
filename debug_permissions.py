#!/usr/bin/env python
"""
Debug script to check and fix Product Batch permissions
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qdpc.settings')
django.setup()

from django.contrib.auth.models import User, Group
from qdpc.models.page_permission import PagePermission
from product.services.permission_service import ProductBatchPermissionService

def debug_permissions():
    print("=== Product Batch Permission Debug ===\n")
    
    # Check current PagePermission records
    print("1. Current PagePermission records for 'Product batch':")
    page_name = ProductBatchPermissionService.PAGE_NAME
    print(f"   Looking for page: '{page_name}'")
    
    permissions = PagePermission.objects.filter(page_name=page_name)
    print(f"   Found {permissions.count()} total permissions")
    
    active_permissions = permissions.filter(is_active=True)
    print(f"   Found {active_permissions.count()} active permissions")
    
    if active_permissions.exists():
        for perm in active_permissions:
            print(f"   - Group: {perm.group.name}, Type: {perm.permission_type}, Active: {perm.is_active}")
    else:
        print("   ⚠ No active permissions found!")
    
    # Check all users and their permissions
    print("\n2. User permission check:")
    users = User.objects.filter(is_active=True)[:5]  # Check first 5 users
    
    for user in users:
        print(f"\n   User: {user.username}")
        print(f"   Is superuser: {user.is_superuser}")
        print(f"   Groups: {[g.name for g in user.groups.all()]}")
        
        # Check edit permission
        has_edit = ProductBatchPermissionService.check_user_permission(user, 'edit')
        print(f"   Has edit permission: {has_edit}")
        
        if not has_edit and not user.is_superuser:
            print("   ⚠ User lacks edit permission!")
    
    # Check if we need to create permissions
    print("\n3. Checking if permissions need to be created:")
    all_groups = Group.objects.all()
    
    for group in all_groups:
        group_perms = PagePermission.objects.filter(
            group=group, 
            page_name=page_name, 
            is_active=True
        )
        
        print(f"   Group '{group.name}': {group_perms.count()} permissions")
        
        if group_perms.count() == 0:
            print(f"   ⚠ Group '{group.name}' has no Product batch permissions!")

def create_default_permissions():
    """Create default permissions for all groups"""
    print("\n=== Creating Default Permissions ===")
    
    page_name = ProductBatchPermissionService.PAGE_NAME
    permission_types = ['view', 'add', 'edit', 'delete', 'approve']
    
    groups = Group.objects.all()
    
    for group in groups:
        print(f"\nCreating permissions for group: {group.name}")
        
        for perm_type in permission_types:
            # Check if permission already exists
            existing = PagePermission.objects.filter(
                group=group,
                page_name=page_name,
                permission_type=perm_type
            ).first()
            
            if not existing:
                # Create new permission
                PagePermission.objects.create(
                    group=group,
                    page_name=page_name,
                    permission_type=perm_type,
                    is_active=True
                )
                print(f"   ✓ Created {perm_type} permission")
            else:
                # Update existing to be active
                existing.is_active = True
                existing.save()
                print(f"   ✓ Updated {perm_type} permission to active")

if __name__ == '__main__':
    debug_permissions()
    
    # Ask if we should create default permissions
    print("\n" + "="*50)
    create_perms = input("Create default permissions for all groups? (y/n): ")
    
    if create_perms.lower() == 'y':
        create_default_permissions()
        print("\n✓ Default permissions created!")
        print("Please restart the Django server and try the edit button again.")
    else:
        print("\nNo permissions created. You may need to manually set up permissions in the admin panel.")
