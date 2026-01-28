from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission


class PagePermission(models.Model):
    """Model to store page permissions for groups"""
    
    PERMISSION_TYPES = [
        ('view', 'View'),
        ('add', 'Add'),
        ('edit', 'Edit'),
        ('delete', 'Delete'),
        ('approve', 'Approve'),
        ('reject', 'Reject'),
    ]
    
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='page_permissions')
    page_name = models.CharField(max_length=100)
    page_url = models.CharField(max_length=200)
    permission_type = models.CharField(max_length=20, choices=PERMISSION_TYPES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['group', 'page_name', 'permission_type']
        verbose_name = 'Page Permission'
        verbose_name_plural = 'Page Permissions'
    
    def __str__(self):
        return f"{self.group.name} - {self.page_name} - {self.permission_type}"
    
    @classmethod
    def get_group_permissions(cls, group):
        """Get all permissions for a specific group"""
        return cls.objects.filter(group=group, is_active=True)
    
    @classmethod
    def get_page_permissions(cls, page_name):
        """Get all permissions for a specific page"""
        return cls.objects.filter(page_name=page_name, is_active=True)
    
    @classmethod
    def has_permission(cls, group, page_name, permission_type):
        """Check if a group has a specific permission for a page"""
        return cls.objects.filter(
            group=group,
            page_name=page_name,
            permission_type=permission_type,
            is_active=True
        ).exists()


class Page(models.Model):
    """Model to store available pages in the system"""
    
    SECTION_CHOICES = [
        ('Pages', 'Pages'),
        ('Product Data Management', 'Product Data Management'),
        ('Miscellaneous Data Management', 'Miscellaneous Data Management'),
        ('User Management', 'User Management'),
        ('Report Generation', 'Report Generation'),
        ('Roles Management', 'Roles Management'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    url = models.CharField(max_length=200)
    section = models.CharField(max_length=50, choices=SECTION_CHOICES)
    page_id = models.IntegerField(unique=True)
    icon = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['page_id']
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'
    
    def __str__(self):
        return f"{self.page_id}. {self.name}"
    
    @classmethod
    def get_pages_by_section(cls):
        """Get all pages organized by section"""
        pages = cls.objects.filter(is_active=True).order_by('page_id')
        sections = {}
        for page in pages:
            if page.section not in sections:
                sections[page.section] = []
            sections[page.section].append(page)
        return sections
    
    def get_group_permissions(self, group):
        """Get all permissions for this page for a specific group"""
        return PagePermission.objects.filter(
            group=group,
            page_name=self.name,
            is_active=True
        )
    
    def has_group_permission(self, group, permission_type):
        """Check if a group has a specific permission for this page"""
        return PagePermission.objects.filter(
            group=group,
            page_name=self.name,
            permission_type=permission_type,
            is_active=True
        ).exists()
