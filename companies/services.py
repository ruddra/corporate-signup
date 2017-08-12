"""
Company Service
"""
import uuid
import os
import logging

from django.conf import settings

from core.services import CoreService

logger = logging.getLogger(__name__)


class CompanyService(CoreService):
    """
    Company Service class
    """
    logger = logger

    def get_file_path(self, instance, filename):
        """
        Change File Names to random UUID Names
        """
        ext = filename.split('.')[-1]
        filename = "{}.{}".format(uuid.uuid4(), ext)
        filepath = settings.MEDIA_ROOT
        return os.path.join(filepath, filename)

    def get_company(self, company_id):
        """ Get Company """
        from companies.models import Company  # to prevent circular dependency
        try:
            return Company.objects.get(pk=company_id)
        except Company.DoesNotExist:
            self.logger_error("Company not found for {}".format(company_id))
            return None
        except Exception as ex:
            self.logger_error("Error: {}".format(str(ex)))
            return None
