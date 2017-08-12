"""
User Service
"""
import logging

from core.services import CoreService
from core.exceptions import ServiceValidationError
from users.models import User
from users.constants import SessionStorageConstants
from companies.services import CompanyService


logger = logging.getLogger(__name__)


class UserService(CoreService):
    logger = logger
    password_min_len = 6

    def validate_email(self, email):
        """
        Validate Email Address
        """
        if email:
            self.logger_info(
                "Found email {}. Running validation check".format(email))
            user = User.objects.filter(email=email)
            if user.exists():
                raise ServiceValidationError("Email Already exists")
            return
        self.logger_error("Email not found")
        raise ServiceValidationError("Email not found")

    def validate_password(self, password1, password2):
        if password1 and password2:
            self.logger_info(
                "Found Passwords Running validation check")
            if password1 != password2:
                raise ServiceValidationError("Passwords do not match")
            elif len(password1) < self.password_min_len:
                raise ServiceValidationError(
                    "Minimum length of password should be 6"
                )
            return
        raise ServiceValidationError("Password not given")

    def get_session_key(self, key):
        """
        Generate Session Keys
        """
        return SessionStorageConstants.STORAGE_KEY.format(key)

    def set_form_data_in_session(self, request, key, value):
        """
        Store Form Data In Session
        """
        request.session[self.get_session_key(key)] = value

    def set_in_session(self, request, key, value):
        """
        Store In Session
        """
        request.session[key] = value

    def get_from_session(self, request, key):
        """
        GET Form Data In Session
        """
        return request.session.get(key, None)

    def get_form_data_in_session(self, request, key):
        """
        Get Form Data from Session
        """
        return request.session.get(self.get_session_key(key), None)

    def reset_form_data_in_session(self, request, key):
        """
        Reset Form Data In session
        """
        del request.session[self.get_session_key(key)]

    def reset_in_session(self, request, key):
        """
        Reset In session
        """
        del request.session[key]

    def clean_up_user_data(self, data):
        """
        Clean Up data
        """
        data.pop('retype_password')
        data.pop('csrfmiddlewaretoken')
        return data

    def create_user(self, request):

        data = self.get_form_data_in_session(
            request,
            SessionStorageConstants.FIRST_STEP_KEY
        )
        try:
            user_data = self.clean_up_user_data(data)
            return User.objects.create_user(**user_data)
        except Exception as exp:
            # Not handling multiple exp for demo purpose
            self.logger_error("Exception: {}".format(str(exp)))
            return None

    def reset_all_session_data(self, request):
        """
        Reset All sessions
        """
        self.reset_form_data_in_session(
            request,
            SessionStorageConstants.FIRST_STEP_KEY)
        self.reset_form_data_in_session(
            request,
            SessionStorageConstants.FIRST_STEP_CLEANED_DATA_KEY
        )
        self.reset_form_data_in_session(
            request,
            SessionStorageConstants.SECOND_STEP_KEY
        )
        self.reset_form_data_in_session(
            request,
            SessionStorageConstants.SECOND_STEP_CLEANED_DATA_KEY
        )
        self.reset_in_session(
            request,
            SessionStorageConstants.COMPANY_ID
        )

        request.session.modified = True

    def check_session_cleared(self, request):
        user = self.get_form_data_in_session(
            request,
            SessionStorageConstants.FIRST_STEP_KEY
        )
        address = self.get_form_data_in_session(
            request,
            SessionStorageConstants.SECOND_STEP_KEY
        )
        company_id = self.get_from_session(
            request,
            SessionStorageConstants.COMPANY_ID
        )
        if user and address and company_id:
            self.logger_info("Keys in Session Exists")
            return False
        self.logger_info("Session Flushed")
        return True
