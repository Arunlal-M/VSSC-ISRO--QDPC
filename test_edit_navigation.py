#!/usr/bin/env python
"""
Test script to debug Product Batch Edit navigation issue
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qdpc.settings')
django.setup()

from django.contrib.auth.models import User
from django.urls import reverse
from qdpc_core_models.models.productBatch import ProductBatchs
from product.services.permission_service import ProductBatchPermissionService

def test_edit_navigation():
    print("=== Product Batch Edit Navigation Test ===\n")
    
    # Test 1: Check if ProductBatchs model is accessible
    print("1. Testing ProductBatchs model access:")
    try:
        batch_count = ProductBatchs.objects.count()
        print(f"   ✓ ProductBatchs model accessible - {batch_count} batches found")
        
        if batch_count > 0:
            first_batch = ProductBatchs.objects.first()
            print(f"   ✓ First batch: ID={first_batch.id}, Batch ID={first_batch.batch_id}")
        else:
            print("   ⚠ No product batches found in database")
    except Exception as e:
        print(f"   ✗ Error accessing ProductBatchs model: {e}")
        return
    
    # Test 2: Check URL reverse
    print("\n2. Testing URL reverse:")
    try:
        if batch_count > 0:
            edit_url = reverse('product-batch-edit', kwargs={'pk': first_batch.id})
            print(f"   ✓ Edit URL generated: {edit_url}")
        else:
            edit_url = reverse('product-batch-edit', kwargs={'pk': 1})
            print(f"   ✓ Edit URL pattern works: {edit_url}")
    except Exception as e:
        print(f"   ✗ Error generating edit URL: {e}")
        return
    
    # Test 3: Check user permissions
    print("\n3. Testing user permissions:")
    try:
        users = User.objects.filter(is_active=True)[:3]
        for user in users:
            print(f"\n   User: {user.username}")
            print(f"   Is superuser: {user.is_superuser}")
            print(f"   Groups: {[g.name for g in user.groups.all()]}")
            
            # Check edit permission
            has_edit = ProductBatchPermissionService.check_user_permission(user, 'edit')
            print(f"   Has edit permission: {has_edit}")
            
            if not has_edit and not user.is_superuser:
                print("   Debug info:")
                debug_info = ProductBatchPermissionService.debug_user_permissions(user)
                print(f"   {debug_info}")
    except Exception as e:
        print(f"   ✗ Error checking permissions: {e}")
    
    # Test 4: Check PagePermission records
    print("\n4. Testing PagePermission records:")
    try:
        from qdpc.models.page_permission import PagePermission
        
        page_name = ProductBatchPermissionService.PAGE_NAME
        print(f"   Looking for page: '{page_name}'")
        
        permissions = PagePermission.objects.filter(page_name=page_name, is_active=True)
        print(f"   Found {permissions.count()} active permissions")
        
        for perm in permissions:
            print(f"   - Group: {perm.group.name}, Type: {perm.permission_type}")
            
    except Exception as e:
        print(f"   ✗ Error checking PagePermission: {e}")

if __name__ == '__main__':
    test_edit_navigation()
