from django.contrib import admin
from .models.page_permission import Page, PagePermission


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['page_id', 'name', 'section', 'url', 'is_active', 'created_at']
    list_filter = ['section', 'is_active', 'created_at']
    search_fields = ['name', 'url', 'description']
    ordering = ['page_id']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('page_id', 'name', 'url', 'section', 'icon', 'description')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PagePermission)
class PagePermissionAdmin(admin.ModelAdmin):
    list_display = ['group', 'page_name', 'permission_type', 'is_active', 'created_at']
    list_filter = ['group', 'permission_type', 'is_active', 'created_at']
    search_fields = ['group__name', 'page_name', 'page_url']
    ordering = ['group__name', 'page_name', 'permission_type']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Permission Details', {
            'fields': ('group', 'page_name', 'page_url', 'permission_type')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('group')
