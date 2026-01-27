from django.contrib.auth.models import Group
from django.db import models

class Role(Group):
    description = models.TextField(blank=True, null=True, help_text="Description of the role")
    is_active = models.BooleanField(default=True, help_text="Whether this role is active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'qdpc_core_models.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_roles'
    )

    class Meta:
        verbose_name_plural = "Roles"
        ordering = ['name']
        proxy = False

    def __str__(self):
        return self.name

    @property
    def is_default(self):
        """Check if this is a default system role"""
        return self.name.upper() in ['GUEST', 'ADMIN', 'QA', 'QC', 'SDA', 'INDUSTRY', 'SUPER ADMIN', 'MASTER ADMIN']

    @property
    def can_be_deleted(self):
        """Check if this role can be deleted (not default and no users assigned)"""
        return not self.is_default and self.user_set.count() == 0

    @property
    def users_count(self):
        """Get the count of users assigned to this role"""
        return self.user_set.count()

    def get_page_permissions(self):
        """Get page permissions for this role using the PagePermission system"""
        from qdpc.models.page_permission import PagePermission
        return PagePermission.objects.filter(group=self, is_active=True)

    def has_page_permission(self, page_name, permission_type):
        """Check if this role has a specific page permission"""
        from qdpc.models.page_permission import PagePermission
        return PagePermission.objects.filter(
            group=self,
            page_name=page_name,
            permission_type=permission_type,
            is_active=True
        ).exists()
        