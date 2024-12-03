from django.db import models

class Unit(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    abbreviation = models.CharField(max_length=10)

    def __str__(self):
        return self.abbreviation
