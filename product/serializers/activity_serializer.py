from rest_framework import serializers
from  qdpc_core_models.models.activitylog import  ActivityLog


class ActivityLogSerializer(serializers.ModelSerializer):
    time = serializers.SerializerMethodField()
    
    class Meta:
        model = ActivityLog
        fields = ['id', 'title', 'description', 'time', 'activity_type', 'action', 'reference_id']
    
    def get_time(self, obj):
        return obj.time_ago




# serializers.py
from rest_framework import serializers
from  qdpc_core_models.models.activity import  Activity

class ActivitySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    content_type = serializers.StringRelatedField()

    class Meta:
        model = Activity
        fields = ['id', 'user', 'action', 'content_type', 'object_id', 'timestamp', 'details']
