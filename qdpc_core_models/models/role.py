from django.contrib.auth.models import Group


class Role(Group):
    class Meta:
        verbose_name_plural = "Roles"
        ordering = ['name']
        proxy = True
    def __unicode__(self):
        return self.name
