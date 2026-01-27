#!/usr/bin/env python
"""
Script to add Guest role to Django Groups
Run this with: python add_guest_role.py
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qdpc.settings')

# Setup Django
django.setup()

from django.contrib.auth.models import Group

def add_guest_role():
    """Add Guest role to Django Groups if it doesn't exist"""
    try:
        # Check if Guest group already exists
        guest_group, created = Group.objects.get_or_create(name='Guest')
        
        if created:
            print(f"✅ Successfully created 'Guest' group with ID: {guest_group.id}")
        else:
            print(f"ℹ️  'Guest' group already exists with ID: {guest_group.id}")
        
        # List all existing groups
        print("\n📋 All existing groups:")
        all_groups = Group.objects.all().order_by('name')
        for group in all_groups:
            print(f"  - {group.name} (ID: {group.id})")
            
        return guest_group
        
    except Exception as e:
        print(f"❌ Error creating Guest group: {e}")
        return None

if __name__ == '__main__':
    print("🔧 Adding Guest role to Django Groups...")
    add_guest_role()
    print("\n✅ Script completed!")
