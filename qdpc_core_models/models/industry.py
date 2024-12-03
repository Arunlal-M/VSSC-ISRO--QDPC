from django.db import models

class Industry(models.Model):
    id = models.AutoField(primary_key=True)  # Use AutoField for primary key
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)  # Allow blank descriptions
    address = models.CharField(max_length=255, blank=True)  # Allow blank addresses
    phone_number = models.CharField(max_length=20, blank=True)  # Allow blank phone numbers

    class Meta:
        verbose_name = 'Industry'
        verbose_name_plural = 'Industries'

    def __str__(self):
        return self.name