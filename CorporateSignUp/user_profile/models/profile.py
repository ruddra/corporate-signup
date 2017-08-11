"""
User Profile Model
"""
from django.db import models

from auth.models import User
from user_profile.models import BillingAddress
from company.models import Company


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
    company = models.ForeignKey(Company)
    billing_address = models.ForeignKey(
        BillingAddress,
        null=True,
        default=None
    )

    def __str__(self):
        return "User: {}, Company: {}".format(self.user, self.company)
