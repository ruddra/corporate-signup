"""
User Profile Model
"""
from django.db import models
from django.utils.translation import ugettext_lazy as _

from users.models import User
from companies.models import Company

from .billing_address import BillingAddress


class Profile(models.Model):
    """
    Profile Model Class
    Why I designed this model like this because:
    1. Keep User Table clean
    2. If I want to use User model in another project, I won't have to worry
       about if there is any relation internally so it would be simply like
       drag and drop
    """
    user = models.OneToOneField(User)
    company = models.ForeignKey(
        Company,
        null=True,
        default=None,
        related_name='company_profiles',
        blank=True  # For avoiding adminsite validation issue
    )
    billing_address = models.ForeignKey(
        BillingAddress,
        null=True,
        default=None,
        related_name="address_profiles",
        blank=True  # same as above
    )

    def __str__(self):
        return "User: {}, Company: {}".format(self.user, self.company)

    class Meta:
        app_label = 'profiles'
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')
