"""
Profile Service
"""
import logging

from core.services import CoreService
from profiles.models import Profile, BillingAddress
from users.services import UserService
from users.constants import SessionStorageConstants

logger = logging.getLogger(__name__)


class ProfileService(CoreService):
    logger = logger  # Configured Logging

    def get_profile(self, user):
        """
        Get User's Profile
        """
        self.logger_info(
            "Initiating Get Profile Method for User {}".format(user.email))
        profiles = Profile.objects.filter(user=user)
        if profiles.exists():
            self.logger_info("Profile Found")
            return profiles.first()  # One to One field, only 1 FK should exist
        self.logger_warning("Profile Not Found")
        return None

    def create_profile(self, user, company, address):
        """
        Create Profile
        """
        try:
            return Profile.objects.create(
                user=user,
                company=company,
                billing_address=address
            )
        except Exception as ex:
            # Possible duplication error
            # Not handling multiple exceptions for now
            self.logger_error("Error: {}".format(str(ex)))

        return None

    def clean_up_profile_data(self, data):
        """
        Pop out unnecessary keys
        """
        data.pop('csrfmiddlewaretoken')
        return data

    def create_address(self, request):
        """
        Create Address
        """
        data = UserService().get_form_data_in_session(
            request,
            SessionStorageConstants.SECOND_STEP_KEY
        )

        cleaned_data = self.clean_up_profile_data(data)

        try:
            return BillingAddress.objects.create(
                **cleaned_data
            )
        except Exception as ex:
            # Possible duplication error
            # Not handling multiple exceptions for now
            self.logger_error("Error: {}".format(str(ex)))

        return None
