from django.db import models


class EndUse(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

class Meta:
    verbose_name = 'Enduse'
    verbose_name_plural = 'Enduses'
    
    def __str__(self):
        return self.name