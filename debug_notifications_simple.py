import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qdpc.settings')
django.setup()

from django.db import connection

try:
    cursor = connection.cursor()
    cursor.execute("DESCRIBE qdpc_core_models_notification")
    columns = [row[0] for row in cursor.fetchall()]
    print("Current columns:", columns)
    
    required = ['title', 'notification_type', 'entity_type']
    missing = [col for col in required if col not in columns]
    
    if missing:
        print("Missing columns:", missing)
        print("Need to run SQL fix!")
    else:
        print("Schema OK - testing notifications...")
        from qdpc_core_models.models.notification import Notification
        count = Notification.objects.count()
        print(f"Total notifications: {count}")
        
except Exception as e:
    print("Error:", e)
