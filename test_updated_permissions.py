import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qdpc.settings')
django.setup()

from django.contrib.auth.models import User, Group
from qdpc.core.permissions import (
    get_role_based_page_access, 
    get_user_accessible_pages_by_role, 
    has_role_based_page_access, 
    ROLE_PAGE_ACCESS
)

print("=== TESTING UPDATED ROLE PERMISSIONS ===\n")

# 1. Show updated role configuration
print("1. UPDATED ROLE CONFIGURATION:")
for role, pages in ROLE_PAGE_ACCESS.items():
    page_count = "ALL PAGES" if pages == ['ALL'] else f"{len(pages)} pages"
    print(f"   {role}: {page_count}")
    if pages != ['ALL']:
        print(f"      Pages: {pages}")

# 2. Test with actual database users
print(f"\n2. TESTING WITH DATABASE USERS:")
users = User.objects.all()[:3]  # Test first 3 users

for user in users:
    print(f"\n   User: {user.username}")
    user_groups = [g.name for g in user.groups.all()]
    print(f"   Groups: {user_groups}")
    print(f"   Superuser: {user.is_superuser}")
    
    # Test get_role_based_page_access
    try:
        accessible_pages = get_role_based_page_access(user)
        print(f"   Accessible pages: {accessible_pages}")
        
        # Test get_user_accessible_pages_by_role
        pages_by_role = get_user_accessible_pages_by_role(user)
        print(f"   Pages by role: {pages_by_role}")
        
        # Test specific page access
        test_pages = ['dashboard', 'equipment', 'reports', 'user_management', 'invalid_page']
        print(f"   Page access tests:")
        for page in test_pages:
            has_access = has_role_based_page_access(user, page)
            print(f"      {page}: {has_access}")
            
    except Exception as e:
        print(f"   ERROR: {e}")

# 3. Test each role in ROLE_PAGE_ACCESS
print(f"\n3. TESTING ROLE CONFIGURATIONS:")
for role_name, expected_pages in ROLE_PAGE_ACCESS.items():
    try:
        group = Group.objects.filter(name=role_name).first()
        if group and group.user_set.exists():
            user = group.user_set.first()
            actual_pages = get_role_based_page_access(user)
            
            # Check if matches expected
            matches = actual_pages == expected_pages
            status = "✓ PASS" if matches else "✗ FAIL"
            print(f"   {role_name}: {status}")
            
            if not matches:
                print(f"      Expected: {expected_pages}")
                print(f"      Got: {actual_pages}")
        else:
            print(f"   {role_name}: No group or users found")
    except Exception as e:
        print(f"   {role_name}: ERROR - {e}")

# 4. Test edge cases
print(f"\n4. TESTING EDGE CASES:")

# Test unauthenticated user
class MockUser:
    def __init__(self, is_authenticated=False, is_superuser=False, groups=None):
        self.is_authenticated = is_authenticated
        self.is_superuser = is_superuser
        self._groups = groups or []
    
    def groups(self):
        return self._groups

# Unauthenticated user
unauth_user = MockUser(is_authenticated=False)
print(f"   Unauthenticated user pages: {get_role_based_page_access(unauth_user)}")
print(f"   Unauthenticated dashboard access: {has_role_based_page_access(unauth_user, 'dashboard')}")

print(f"\n=== TESTING COMPLETE ===")
