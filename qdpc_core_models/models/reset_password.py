from .user import User
from django.db import models


class ResetPassword(models.Model):
    USED_STATUS = (
        (0, "UNUSED"),
        (1, "USED"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reset_key = models.CharField(max_length=50, null=True, blank=True)
    used_status = models.CharField(choices=USED_STATUS, max_length=100,
                                   default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Reset Password"

    def __str__(self):
        return self.reset_key
