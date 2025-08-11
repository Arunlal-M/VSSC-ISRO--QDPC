from django.contrib.auth.models import Group
from django.db import models

class Role(Group):
    class Meta:
        verbose_name_plural = "Roles"
        ordering = ['name']
        proxy = True  # This means Role won't create a new DB table

    def __str__(self):
        return self.name
    
    @property
    def is_default(self):
        return self.name in ['GUEST', 'ADMIN', 'QA', 'QC', 'SDA', 'INDUSTRY']
        