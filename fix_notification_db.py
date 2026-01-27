#!/usr/bin/env python
"""
Script to fix notification database schema issues
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qdpc.settings')
django.setup()

from django.db import connection

def fix_notification_schema():
    """Add missing columns to notification table"""
    with connection.cursor() as cursor:
        try:
            # Check if columns exist first
            cursor.execute("DESCRIBE qdpc_core_models_notification")
            existing_columns = [row[0] for row in cursor.fetchall()]
            
            print(f"Existing columns: {existing_columns}")
            
            # Add missing columns if they don't exist
            columns_to_add = [
                ("title", "ALTER TABLE qdpc_core_models_notification ADD COLUMN title VARCHAR(200) DEFAULT 'Notification'"),
                ("notification_type", "ALTER TABLE qdpc_core_models_notification ADD COLUMN notification_type VARCHAR(20) DEFAULT 'create'"),
                ("entity_type", "ALTER TABLE qdpc_core_models_notification ADD COLUMN entity_type VARCHAR(50) DEFAULT 'product_batch'"),
                ("entity_id", "ALTER TABLE qdpc_core_models_notification ADD COLUMN entity_id INTEGER NULL"),
                ("entity_name", "ALTER TABLE qdpc_core_models_notification ADD COLUMN entity_name VARCHAR(200) DEFAULT ''"),
                ("created_by_id", "ALTER TABLE qdpc_core_models_notification ADD COLUMN created_by_id INTEGER NULL"),
            ]
            
            for column_name, sql in columns_to_add:
                if column_name not in existing_columns:
                    print(f"Adding column: {column_name}")
                    cursor.execute(sql)
                else:
                    print(f"Column {column_name} already exists")
            
            # Modify message column to TEXT if needed
            cursor.execute("ALTER TABLE qdpc_core_models_notification MODIFY COLUMN message TEXT")
            print("Modified message column to TEXT")
            
            print("Database schema updated successfully!")
            
        except Exception as e:
            print(f"Error updating schema: {e}")
            return False
    
    return True

if __name__ == "__main__":
    fix_notification_schema()
