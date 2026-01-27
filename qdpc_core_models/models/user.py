from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from .division import Division
from .center import Center
from .role import Role
from .user_type import UserType


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The username field is required')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_approved', True)

        if password is None:
            raise ValueError('Superuser must have a password')

        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    SALUTATION_CHOICES = (
        ('Mr.', 'Mr.'),
        ('Ms.', 'Ms.'),
        ('Dr.', 'Dr.'),
    )

    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    desired_salutation = models.CharField(max_length=10, choices=SALUTATION_CHOICES, default='Mr.')
    user_id = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(max_length=150, unique=True)
    centre = models.ManyToManyField(Center, related_name='users', blank=True)
    divisions = models.ManyToManyField(Division, related_name='users', blank=True)
    phone_regex = RegexValidator(regex=r'\d{0,20}$', message="Phone number can be blank or in international format.")
    phone_number = models.CharField(max_length=20, validators=[phone_regex], blank=True)
    date_joined = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    # Use ForeignKey for Role
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
        verbose_name="Role"
    )

    usertype = models.ForeignKey(UserType, on_delete=models.CASCADE, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.username
    
    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between."""
        full_name = f'{self.first_name} {self.last_name}'.strip()
        return full_name if full_name else self.username
    
    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name if self.first_name else self.username
