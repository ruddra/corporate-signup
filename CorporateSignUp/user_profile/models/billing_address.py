"""
Billing Address Model
"""
from django.db import models
from django_countries.fields import CountryField

from core.models import CoreModel


class BillingAddress(CoreModel):
    """
    Billing Address Class
    """
    address = models.CharField(
        verbose_name="Address",
        help_text="Address",
        max_length=255
    )
    current_city = models.CharField(
        verbose_name="City",
        help_text="City",
        max_length=255,
        null=True,
        default=None
    )
    country = CountryField()
