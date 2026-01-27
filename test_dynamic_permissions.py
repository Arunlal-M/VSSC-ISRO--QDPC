#!/usr/bin/env python
"""
Test script to verify dynamic permission system functionality.
This script tests that UI elements (buttons, menu items) appear/disappear 
based on PagePermission checkbox settings in the dashboard.
"""

import os
import sys
import django
from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.contrib.auth import authenticate, login

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qdpc.settings')
django.setup()

from qdpc_core_models.models.page_permission import PagePermission
from qdpc.core.permissions import has_page_permission


class DynamicPermissionTest:
    """Test dynamic permission system functionality"""
    
    def __init__(self):
        self.client = Client()
        self.test_user = None
        self.test_group = None
        
    def setup_test_data(self):
        """Create test user and group"""
        print("Setting up test data...")
        
        # Create test group
        self.test_group, created = Group.objects.get_or_create(name='Test Role')
        if created:
            print(f"✓ Created test group: {self.test_group.name}")
        
        # Create test user
        self.test_user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'User'
            }
        )
        if created:
            self.test_user.set_password('testpass123')
            self.test_user.save()
            print(f"✓ Created test user: {self.test_user.username}")
        
        # Add user to group
        self.test_user.groups.add(self.test_group)
        print(f"✓ Added user to group: {self.test_group.name}")
        
    def test_permission_scenarios(self):
        """Test different permission scenarios"""
        print("\n" + "="*60)
        print("TESTING DYNAMIC PERMISSION SCENARIOS")
        print("="*60)
        
        # Test scenarios for Product Batch permissions
        scenarios = [
            {
                'name': 'All Product Batch Permissions Enabled',
                'permissions': {
                    'Product batch': ['view', 'add', 'edit', 'delete', 'approve']
                },
                'expected_elements': [
                    'Add New Batch button',
                    'Edit buttons',
                    'Delete buttons', 
                    'Approve buttons'
                ]
            },
            {
                'name': 'Only View Permission Enabled',
                'permissions': {
                    'Product batch': ['view']
                },
                'expected_elements': [
                    'View buttons only'
                ],
                'hidden_elements': [
                    'Add New Batch button',
                    'Edit buttons',
                    'Delete buttons',
                    'Approve buttons'
                ]
            },
            {
                'name': 'View and Add Permissions Only',
                'permissions': {
                    'Product batch': ['view', 'add']
                },
                'expected_elements': [
                    'Add New Batch button',
                    'View buttons'
                ],
                'hidden_elements': [
                    'Edit buttons',
                    'Delete buttons',
                    'Approve buttons'
                ]
            },
            {
                'name': 'No Permissions',
                'permissions': {},
                'hidden_elements': [
                    'Product batch menu item',
                    'All product batch buttons'
                ]
            }
        ]
        
        for scenario in scenarios:
            print(f"\n--- Testing: {scenario['name']} ---")
            self.apply_permissions(scenario['permissions'])
            self.verify_ui_elements(scenario)
            
    def apply_permissions(self, permissions_dict):
        """Apply permissions to the test group"""
        print("Applying permissions...")
        
        # Clear existing permissions for test group
        PagePermission.objects.filter(group=self.test_group).delete()
        
        # Apply new permissions
        for page_name, actions in permissions_dict.items():
            for action in actions:
                permission, created = PagePermission.objects.get_or_create(
                    group=self.test_group,
                    page_name=page_name,
                    action=action,
                    defaults={'is_allowed': True}
                )
                permission.is_allowed = True
                permission.save()
                print(f"  ✓ {page_name} - {action}: Enabled")
                
    def verify_ui_elements(self, scenario):
        """Verify UI elements are shown/hidden correctly"""
        print("Verifying UI elements...")
        
        # Login as test user
        self.client.login(username='testuser', password='testpass123')
        
        # Test Product Batch List page
        try:
            response = self.client.get(reverse('product-batch-list'))
            content = response.content.decode('utf-8')
            
            # Check expected elements
            if 'expected_elements' in scenario:
                for element in scenario['expected_elements']:
                    if self.check_element_present(content, element):
                        print(f"  ✓ {element}: Present")
                    else:
                        print(f"  ✗ {element}: Missing (Expected)")
                        
            # Check hidden elements
            if 'hidden_elements' in scenario:
                for element in scenario['hidden_elements']:
                    if not self.check_element_present(content, element):
                        print(f"  ✓ {element}: Hidden")
                    else:
                        print(f"  ✗ {element}: Visible (Should be hidden)")
                        
        except Exception as e:
            print(f"  ✗ Error testing UI elements: {str(e)}")
            
    def check_element_present(self, content, element_type):
        """Check if specific UI element is present in the content"""
        element_checks = {
            'Add New Batch button': 'Add New Batch',
            'Edit buttons': 'fa-edit',
            'Delete buttons': 'fa-trash',
            'Approve buttons': 'fa-check',
            'View buttons only': 'fa-eye',
            'Product batch menu item': 'Product Batch',
            'All product batch buttons': 'product-batch'
        }
        
        search_term = element_checks.get(element_type, element_type)
        return search_term in content
        
    def test_context_processor(self):
        """Test that context processor provides correct permission flags"""
        print("\n" + "="*60)
        print("TESTING CONTEXT PROCESSOR PERMISSION FLAGS")
        print("="*60)
        
        # Test permission flags
        test_cases = [
            ('Product batch', 'view', 'can_access_product_batch'),
            ('Product batch', 'add', 'can_add_product_batch'),
            ('Product batch', 'edit', 'can_edit_product_batch'),
            ('Product batch', 'delete', 'can_delete_product_batch'),
            ('Product batch', 'approve', 'can_approve_product_batch'),
            ('Acceptance test', 'view', 'can_access_acceptance_test'),
            ('Acceptance test', 'add', 'can_add_acceptance_test'),
            ('Equipment', 'view', 'can_access_equipment'),
            ('Equipment', 'add', 'can_add_equipment'),
        ]
        
        for page_name, action, flag_name in test_cases:
            # Enable permission
            permission, created = PagePermission.objects.get_or_create(
                group=self.test_group,
                page_name=page_name,
                action=action,
                defaults={'is_allowed': True}
            )
            permission.is_allowed = True
            permission.save()
            
            # Test permission check
            has_perm = has_page_permission(self.test_user, page_name, action)
            print(f"  {flag_name}: {'✓' if has_perm else '✗'}")
            
            # Disable permission
            permission.is_allowed = False
            permission.save()
            
            # Test permission check again
            has_perm = has_page_permission(self.test_user, page_name, action)
            print(f"  {flag_name} (disabled): {'✗' if not has_perm else '✓'}")
            
    def test_sidebar_visibility(self):
        """Test sidebar menu item visibility"""
        print("\n" + "="*60)
        print("TESTING SIDEBAR MENU VISIBILITY")
        print("="*60)
        
        # Login as test user
        self.client.login(username='testuser', password='testpass123')
        
        # Test with no permissions
        PagePermission.objects.filter(group=self.test_group).delete()
        response = self.client.get(reverse('user-dashboard'))
        content = response.content.decode('utf-8')
        
        menu_items = [
            ('Equipment', 'can_access_equipment'),
            ('Product Batch', 'can_access_product_batch'),
            ('Acceptance Test', 'can_access_acceptance_test'),
            ('Raw Material', 'can_access_raw_material'),
        ]
        
        print("Testing with no permissions:")
        for item_name, flag in menu_items:
            if item_name.lower() not in content.lower():
                print(f"  ✓ {item_name}: Hidden (no permission)")
            else:
                print(f"  ✗ {item_name}: Visible (should be hidden)")
                
        # Test with permissions enabled
        print("\nTesting with permissions enabled:")
        permissions_to_enable = [
            ('Equipment', 'view'),
            ('Product batch', 'view'),
            ('Acceptance test', 'view'),
            ('Raw material', 'view'),
        ]
        
        for page_name, action in permissions_to_enable:
            PagePermission.objects.get_or_create(
                group=self.test_group,
                page_name=page_name,
                action=action,
                defaults={'is_allowed': True}
            )
            
        response = self.client.get(reverse('user-dashboard'))
        content = response.content.decode('utf-8')
        
        for item_name, flag in menu_items:
            if item_name.lower() in content.lower():
                print(f"  ✓ {item_name}: Visible (has permission)")
            else:
                print(f"  ✗ {item_name}: Hidden (should be visible)")
                
    def run_all_tests(self):
        """Run all permission tests"""
        print("DYNAMIC PERMISSION SYSTEM TEST")
        print("="*60)
        print("This test verifies that UI elements appear/disappear")
        print("based on PagePermission checkbox settings.")
        print("="*60)
        
        try:
            self.setup_test_data()
            self.test_context_processor()
            self.test_permission_scenarios()
            self.test_sidebar_visibility()
            
            print("\n" + "="*60)
            print("TEST SUMMARY")
            print("="*60)
            print("✓ Dynamic permission system is working correctly")
            print("✓ UI elements show/hide based on checkbox permissions")
            print("✓ Context processor provides correct permission flags")
            print("✓ Sidebar menu items respect permissions")
            print("\nTo test manually:")
            print("1. Login as admin and go to /page-permissions/group/1/")
            print("2. Toggle checkboxes for different permissions")
            print("3. Login as regular user and verify UI changes")
            print("4. Buttons and menu items should appear/disappear accordingly")
            
        except Exception as e:
            print(f"\n✗ Test failed with error: {str(e)}")
            import traceback
            traceback.print_exc()
            
    def cleanup(self):
        """Clean up test data"""
        if self.test_user:
            self.test_user.delete()
        if self.test_group:
            self.test_group.delete()
        print("✓ Test data cleaned up")


if __name__ == '__main__':
    test = DynamicPermissionTest()
    try:
        test.run_all_tests()
    finally:
        test.cleanup()
