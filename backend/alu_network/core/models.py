"""
DATABASE MODELS
"""
import tldextract
from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    """
    Custom UserManager model that manages user profile
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates a new user.
        """

        if not email:
            raise ValueError('User must have an email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """
        Creates a super User
        """
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model.
    """

    USER_ROLE_CHOICES = [
        ('student', 'Student'),
        ('staff', 'Staff'),
        ('alumni', 'Alumni'),
    ]


    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    short_bio = models.CharField(max_length=255, blank=True)
    about_me = models.TextField(blank=True)
    user_role = models.CharField(
        max_length=10,
        choices=USER_ROLE_CHOICES,
    )
    intake = models.CharField(max_length=20, blank=True)
    professional_role = models.CharField(max_length=255, blank=True, help_text="Your role at your current company.")
    current_company = models.CharField(max_length=255, blank=True)

    # Pictures are coming soon
    # picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    # background_image = models.ImageField(upload_to='background_pics/', blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'

    # properties I want to add either here or in the serializer class
    #('followers', 'following', 'connections', 'last_active', 'number_of_post', )

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name}"

    def __str__(self):
        """String representation of a user"""
        return f"{self.full_name} - {self.email}"


class Link(models.Model):
    """
    Model for user's social media links
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.URLField(blank=True, help_text="The name will be gotten \
        from the URL domain. Edit only if you want something different.")
    url = models.URLField()

    def save(self, *args, **kwargs):
        """
        Override the save method to set the name from URL if not provided
        """
        if not self.name:
            ext = tldextract.extract(self.url)
            domain = ext.domain.capitalize()
            self.name = domain
        super().save(*args, **kwargs)

    def __str__(self):
        """String representation of a link"""
        return f"{str(self.user)} {self.name} Link"
