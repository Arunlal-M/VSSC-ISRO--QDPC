from django.db import models
from .center import Center

class Division(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150,unique=True)
    center = models.ForeignKey(Center, on_delete=models.CASCADE, related_name='divisions')  # Link to Center

    class Meta:
        verbose_name = 'Division'
        verbose_name_plural = 'Divisions'

    def __str__(self):
        return self.name