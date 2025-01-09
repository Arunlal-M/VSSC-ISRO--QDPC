from django.db import models

class DocumentType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    
class Meta:
    verbose_name = 'DocumentType'
    verbose_name_plural = 'DocumentTypes'

def __str__(self):
    return self.name


