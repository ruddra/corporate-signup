"""
Company Model
"""
from django.db import models

from core.models import CoreModel
from company.constants import CompanyType


class Company(CoreModel):
    """
    Company Model Class
    """
    name = models.CharField(
        verbose_name="Company",
        max_length=255
    )
    logo = models.FileField(
        verbose_name="Company Logo"
    )
    description = models.TextField()
    company_type = models.IntegerField(
        verbose_name="Type",
        help_text="Please choose from Business entities for this company",
        choices=CompanyType.choices,
        default=CompanyType.PUBLIC
    )

    def __str__(self):
        return self.name
