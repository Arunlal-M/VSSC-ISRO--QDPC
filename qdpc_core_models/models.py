
from django.db import models
from django.contrib.auth.models import Group

class RoleMeta(models.Model):
    group = models.OneToOneField(
        Group,
        on_delete=models.CASCADE,
        related_name='role_meta'  # unique name to avoid reverse accessor clash
    )
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.group.name} (Default: {self.is_default})"
