#!/usr/bin/env python
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qdpc.settings')
django.setup()

from django.contrib.auth.models import User, Group
from qdpc.core.permissions import (
    get_role_based_page_access, 
    get_user_accessible_pages_by_role, 
    has_role_based_page_access, 
    ROLE_PAGE_ACCESS
)

# Check current database state
print("=== DATABASE STATE ===")
print(f"Total Groups: {Group.objects.count()}")
print(f"Groups: {[g.name for g in Group.objects.all()]}")
print(f"Total Users: {User.objects.count()}")

# Check if required roles exist
print("\n=== ROLE VALIDATION ===")
required_roles = list(ROLE_PAGE_ACCESS.keys())
existing_roles = [g.name for g in Group.objects.all()]

missing_roles = [role for role in required_roles if role not in existing_roles]
print(f"Required roles: {required_roles}")
print(f"Existing roles: {existing_roles}")
print(f"Missing roles: {missing_roles}")

# Test permission functions
print("\n=== PERMISSION FUNCTION TESTS ===")
if User.objects.exists():
    test_user = User.objects.first()
    print(f"Testing with user: {test_user.username}")
    print(f"User groups: {[g.name for g in test_user.groups.all()]}")
    print(f"Is superuser: {test_user.is_superuser}")
    
    # Test each function
    try:
        pages = get_role_based_page_access(test_user)
        print(f"get_role_based_page_access: {pages}")
    except Exception as e:
        print(f"ERROR in get_role_based_page_access: {e}")
    
    try:
        pages_by_role = get_user_accessible_pages_by_role(test_user)
        print(f"get_user_accessible_pages_by_role: {pages_by_role}")
    except Exception as e:
        print(f"ERROR in get_user_accessible_pages_by_role: {e}")
    
    try:
        has_dashboard = has_role_based_page_access(test_user, "dashboard")
        has_equipment = has_role_based_page_access(test_user, "equipment")
        print(f"has_role_based_page_access (dashboard): {has_dashboard}")
        print(f"has_role_based_page_access (equipment): {has_equipment}")
    except Exception as e:
        print(f"ERROR in has_role_based_page_access: {e}")

# Create missing groups if needed
if missing_roles:
    print(f"\n=== CREATING MISSING ROLES ===")
    for role in missing_roles:
        group, created = Group.objects.get_or_create(name=role)
        print(f"{'Created' if created else 'Already exists'}: {role}")

print("\n=== ROLE CONFIGURATION ===")
for role, pages in ROLE_PAGE_ACCESS.items():
    print(f"{role}: {len(pages)} pages - {pages}")
