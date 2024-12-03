from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from .division import Division
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from .center import Center
from .role import Role
from .user_type import UserType


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        """
        Creates and saves a User with the given username, password and extra fields.
        """
        if not username:
            raise ValueError('The username field is required')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        """
        Creates and saves a SuperUser with the given username, password and extra fields.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if password is None:
            raise ValueError('Superuser must have a password')

        return self.create_user(username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """User model"""
   
    SALUTATION_CHOICES = (
        ('Mr.', 'Mr.'),
        ('Ms.', 'Ms.'),
        ('Dr.','Dr.')
        # Add more options as needed
    )

   
    username = models.CharField(
        ('username'),
        max_length=254,
        unique=True,
        error_messages={
            'unique':("A user with that username already exists."),
        },
    )
    desired_salutation = models.CharField(max_length=10, choices=SALUTATION_CHOICES, default='Mr.')
    user_id = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True)  # Consider adding unique=True
    centre = models.ManyToManyField(Center, related_name='users', blank=True)
    divisions = models.ManyToManyField(Division, related_name='users', blank=True,null=True)
    phone_regex = RegexValidator(regex=r'\d{0,20}$', message="Phone number can be blank or in international format.")  # More generic validation
    phone_number = models.CharField(max_length=20, validators=[phone_regex], blank=True)
    date_joined = models.DateField(auto_now_add=True)  # Join date (automatically set)
    is_active = models.BooleanField(default=True)  # Active user status
    # Custom fields
    role_id = models.CharField(max_length=255, null=True, blank=True)  # Role ID (consider using a separate model for roles)
    usertype = models.ForeignKey(UserType, on_delete=models.CASCADE, blank=True, null=True)
    is_staff = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=True) 
    role = models.ManyToManyField(Role, related_name="test_group", verbose_name="Roles", help_text='Hold down "Control", or "Command" on a Mac, to select more than one.')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = UserManager()

   

    def __str__(self):
        return self.username