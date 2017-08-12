"""
Company Model
"""
from django.utils.translation import ugettext_lazy as _
from django.db import models

from core.models import CoreModel
from companies.constants import CompanyType
from companies.services import CompanyService


class Company(CoreModel):
    """
    Company Model Class
    """
    name = models.CharField(
        verbose_name=_("Company Name"),
        max_length=255
    )
    logo = models.FileField(
        verbose_name=_("Company Logo"),
        upload_to=CompanyService().get_file_path
    )
    short_description = models.CharField(
        verbose_name=_("Short Description"),
        help_text=_("Short Description"),
        max_length=800,
        null=True,
        default=None
    )
    description = models.TextField()
    company_type = models.IntegerField(
        verbose_name=_("Type"),
        help_text=_("Please choose from Business entities for this company"),
        choices=CompanyType.choices,
        default=CompanyType.PUBLIC
    )
    is_active = models.BooleanField(
        default=True,
        help_text=_("Is active for subscriptions")
    )

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'companies'
        verbose_name = _('company')
        verbose_name_plural = _('companies')
