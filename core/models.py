"""
Core Model
"""
from django.db import models


class CoreModel(models.Model):
    """
    Core Model Structure. Contains Common Information, such
    as date Created and Last Updated
    """
    date_created = models.DateTimeField(auto_now=True)
    last_updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        app_label = 'Core'
