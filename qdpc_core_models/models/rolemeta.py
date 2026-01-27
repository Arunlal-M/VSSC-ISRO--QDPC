# qdpc_core_models/models/rolemeta.py
from django.db import models
from django.contrib.auth.models import Group

# NOTE: RoleMeta DB table is now created by migration 0016. This model remains for ORM usage.
class RoleMeta(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name='role_meta')
    is_default = models.BooleanField(default=False)
    page_codes = models.TextField(blank=True, null=True, help_text="Comma-separated page codes or 'ALL'")

    def __str__(self):
        return f"{self.group.name} (Default: {self.is_default})"

    # Note: numeric page permissions removed
