
from django.db import models

class ProductComponent(models.Model):
    component_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.component_name