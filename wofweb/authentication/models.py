from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class AccountManager(BaseUserManager):
    """Account manager for user class."""

    def create_user(self, email, password=None, **kwargs):
        """Overload of create user."""
        if not email:
            raise ValueError('Users must have a valid email address')

        if not kwargs.get('username'):
            raise ValueError('Users must have a valid username.')

        account = self.model(
            email=self.normalize_email(email), username=kwargs.get('username'))

        account.set_password(password)
        account.save()

        return account

    def create_superuser(self, email, password, **kwargs):
        """Overload create super user."""
        account = self.create_user(email, password, **kwargs)

        account.is_admin = True
        account.save()

        return account


class Account(AbstractBaseUser):
    """Overloaded user class."""
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40, unique=True)

    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    tagline = models.CharField(max_length=40, blank=True)

    is_admin = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __unicode__(self):
        return self.username

    def get_full_name(self):
        return ' '.join(self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name
