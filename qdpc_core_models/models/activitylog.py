from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class ActivityLog(models.Model):
    # Activity types for easy filtering
    ACTIVITY_TYPES = [
        ('equipment', 'Equipment'),
        ('raw_material', 'Raw Material'),
        ('consumable', 'Consumable'),
        ('product', 'Product'),
        ('maintenance', 'Maintenance'),
        ('alert', 'Alert'),
    ]

    # Action types
    ACTION_TYPES = [
        ('create', 'Created'),
        ('update', 'Updated'),
        ('delete', 'Deleted'),
        ('receive', 'Received'),
        ('complete', 'Completed'),
        ('schedule', 'Scheduled'),
        ('alert', 'Alert'),
    ]

    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='activities'
    )
    activity_type = models.CharField(
        max_length=20, 
        choices=ACTIVITY_TYPES,
        default='equipment'
    )
    action = models.CharField(
        max_length=20, 
        choices=ACTION_TYPES,
        default='create'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    reference_id = models.CharField(max_length=50, blank=True)  # e.g., batch ID, equipment ID
    timestamp = models.DateTimeField(default=timezone.now)
    metadata = models.JSONField(default=dict, blank=True)  # For additional data

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Activity Log'
        verbose_name_plural = 'Activity Logs'

    def __str__(self):
        return f"{self.get_action_display()} {self.get_activity_type_display()}: {self.title}"

    @property
    def time_ago(self):
        """Human-readable time difference"""
        now = timezone.now()
        diff = now - self.timestamp
        
        if diff.days > 0:
            return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
        elif diff.seconds >= 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff.seconds >= 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "Just now"