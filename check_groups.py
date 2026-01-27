#!/usr/bin/env python
"""
Script to check Django Groups and identify any with empty names
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

def check_groups():
    """Check all Django Groups and identify any issues"""
    try:
        print("🔍 Checking all Django Groups...")
        print("=" * 50)
        
        # Get all groups
        all_groups = Group.objects.all().order_by('id')
        
        if not all_groups.exists():
            print("❌ No groups found in database")
            return
        
        print(f"📊 Found {all_groups.count()} groups:")
        print("-" * 50)
        
        for group in all_groups:
            # Check if name is empty or None
            name_status = "✅ OK" if group.name and group.name.strip() else "❌ EMPTY NAME"
            name_display = group.name if group.name else "NO NAME"
            
            print(f"ID: {group.id:2d} | Name: '{name_display}' | Status: {name_status}")
            
            # Check for potential issues
            if not group.name:
                print(f"    ⚠️  Group ID {group.id} has no name!")
            elif not group.name.strip():
                print(f"    ⚠️  Group ID {group.id} has only whitespace in name!")
        
        print("-" * 50)
        
        # Check for groups with empty names
        empty_name_groups = Group.objects.filter(name__isnull=True) | Group.objects.filter(name='')
        if empty_name_groups.exists():
            print(f"🚨 Found {empty_name_groups.count()} groups with empty names:")
            for group in empty_name_groups:
                print(f"    - Group ID: {group.id}, Name: '{group.name}'")
        else:
            print("✅ All groups have valid names")
            
    except Exception as e:
        print(f"❌ Error checking groups: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    check_groups()
    print("\n✅ Script completed!")
