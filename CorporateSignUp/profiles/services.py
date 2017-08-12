"""
Profile Service
"""
import logging

from core.services import CoreService
from profiles.models import Profile

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
