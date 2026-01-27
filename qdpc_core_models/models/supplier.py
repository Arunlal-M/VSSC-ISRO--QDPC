from django.db import models

class Suppliers(models.Model):
     id = models.AutoField(primary_key=True)
     name = models.CharField(max_length=255)
     email = models.EmailField(max_length=191, unique=True) 
     address = models.CharField(max_length=500)
     



     class Meta:
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'

     def __str__(self):
        return self.name
