# views.py
from rest_framework import generics, permissions
from .models import Activity
from product.serializers.activity_serializer import ActivitySerializer

class RecentActivityAPIView(generics.ListAPIView):
    queryset = Activity.objects.select_related('user', 'content_type')[:50]  # Show last 50
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]
