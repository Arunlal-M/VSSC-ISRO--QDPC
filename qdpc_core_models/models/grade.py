from django.db import models

class Grade(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    abbreviation = models.CharField(max_length=10)
    
class Meta:
    verbose_name = 'Grade'
    verbose_name_plural = 'Grades'

def __str__(self):
    return self.name


