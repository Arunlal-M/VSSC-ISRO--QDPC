from django.contrib import admin
from .models import *
from .models.notification import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['message', 'user', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['message', 'user__username']
    readonly_fields = ['created_at']

@admin.register(UserType)
class UserTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)