#!/usr/bin/env python
"""
Script to test notification system functionality
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qdpc.settings')
django.setup()

from django.contrib.auth import get_user_model
from qdpc_core_models.models.notification import Notification
from qdpc.services.notification_service import NotificationService

def test_notification_system():
    """Test notification creation and retrieval"""
    User = get_user_model()
    
    print("=== Testing Notification System ===")
    
    # Check if notification table exists and has correct schema
    try:
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("DESCRIBE qdpc_core_models_notification")
        columns = [row[0] for row in cursor.fetchall()]
        print(f"Notification table columns: {columns}")
        
        # Check if required columns exist
        required_columns = ['title', 'notification_type', 'entity_type', 'entity_id', 'entity_name', 'created_by_id']
        missing_columns = [col for col in required_columns if col not in columns]
        
        if missing_columns:
            print(f"❌ Missing columns: {missing_columns}")
            print("Please run the SQL script to fix the database schema!")
            return False
        else:
            print("✅ All required columns exist")
            
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False
    
    # Test getting users
    try:
        users = User.objects.filter(is_active=True)[:3]
        print(f"Found {users.count()} active users")
        
        if not users:
            print("❌ No active users found")
            return False
            
    except Exception as e:
        print(f"❌ Error getting users: {e}")
        return False
    
    # Test notification creation
    try:
        test_user = users.first()
        print(f"Testing with user: {test_user.username}")
        
        # Create a test notification directly
        notification = Notification.objects.create(
            user=test_user,
            title="Test Notification",
            message="This is a test notification",
            notification_type="create",
            entity_type="product_batch",
            entity_id=1,
            entity_name="Test Batch",
            created_by=test_user
        )
        
        print(f"✅ Created test notification: {notification.id}")
        
        # Test retrieval
        user_notifications = Notification.objects.filter(user=test_user)
        print(f"✅ User has {user_notifications.count()} notifications")
        
        # Test unread count
        unread_count = Notification.get_unread_count(test_user)
        print(f"✅ Unread count: {unread_count}")
        
        # Test NotificationService
        service_notifications = NotificationService.get_user_notifications(test_user, limit=5)
        print(f"✅ NotificationService returned {len(service_notifications)} notifications")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating/testing notifications: {e}")
        return False

if __name__ == "__main__":
    success = test_notification_system()
    if success:
        print("\n🎉 Notification system test completed successfully!")
    else:
        print("\n💥 Notification system test failed!")
