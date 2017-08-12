"""
Billing Address Model
"""
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django_countries.fields import CountryField

from core.models import CoreModel


class BillingAddress(CoreModel):
    """
    Billing Address Class
    """
    address = models.CharField(
        verbose_name=_("Address"),
        help_text=_("Address"),
        max_length=255
    )
    current_city = models.CharField(
        verbose_name=_("City"),
        help_text=_("City"),
        max_length=255,
        null=True,
        default=None
    )
    country = CountryField()

    def __str__(self):
        return 'Address: {} \n City: {} \n Country: {}'.format(
            self.address, self.current_city, self.country
        )

    class Meta:
        app_label = 'profiles'
        verbose_name = _('Billing Address')
        verbose_name_plural = _('Billing Addresses')
