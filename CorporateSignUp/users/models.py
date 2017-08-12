from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser

from core.models import CoreModel


class UserManager(BaseUserManager):
    def _create_user(self, email, password,
                     first_name=None, last_name=None, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        Internal Method
        """
        if not email:
            raise ValueError(_('User must have an email address'))
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name,
                          last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, first_name=None,
                    last_name=None, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)

        return self._create_user(email, password,
                                 first_name, last_name, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Create Super User
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, CoreModel):
    """
    User Model
    """
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(
        verbose_name=_("First Name"),
        max_length=14,
        null=True,
        default=None
    )
    last_name = models.CharField(
        verbose_name=_("Last Name"),
        max_length=14,
        null=True,
        default=None
    )

    objects = UserManager()
    USERNAME_FIELD = 'email'

    def get_full_name(self):
        # The user is identified by their email address
        return '{} {}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):  # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        # Simplest possible answer: Yes, always
        return True

    class Meta:
        app_label = 'users'
        verbose_name = _('User')
        verbose_name_plural = _('Users')
