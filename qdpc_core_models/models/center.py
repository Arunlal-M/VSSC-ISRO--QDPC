from django.db import models
from .user_type import UserType

class Center(models.Model):
    id = models.AutoField(primary_key=True)
    user_type = models.ForeignKey(UserType, on_delete=models.CASCADE)  # Link to Center
    name = models.CharField(max_length=255,unique=True)

    def __str__(self):
        return self.name