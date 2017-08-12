"""
User View
"""
import logging

from django.http import Http404, HttpResponseServerError
from django.http import HttpResponseRedirect
from formtools.wizard.views import SessionWizardView
from formtools.preview import FormPreview
from collections import OrderedDict
from django.views.generic import TemplateView, FormView

from users.services import UserService
from users.constants import SessionStorageConstants
from users.forms import UserForm
from profiles.forms import BillForm
from profiles.services import ProfileService
from companies.services import CompanyService

logger = logging.getLogger(__name__)


class UserSignUpView(FormView):
    form_class = UserForm
    template_name = 'signup/signup.html'
    success_url = '/billing-address'

    def get(self, request, company_id, *args, **kwargs):
        # Setting Company ID in Session
        # Also overriding to get pre-populated data
        company = CompanyService().get_company(company_id)
        if not company:
            raise Http404("Company does not exist")
        UserService().set_in_session(
            request,
            SessionStorageConstants.COMPANY_ID,
            company.id
        )
        data = UserService().get_form_data_in_session(
            request,
            SessionStorageConstants.FIRST_STEP_KEY
        )
        if data:
            self.initial = data

        self.initial['company_id'] = company_id

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_id'] = UserService().get_from_session(
            self.request,
            SessionStorageConstants.COMPANY_ID
        )
        return context

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        UserService().set_form_data_in_session(
            self.request,
            SessionStorageConstants.FIRST_STEP_KEY,
            form.data
        )

        UserService().set_form_data_in_session(
            self.request,
            SessionStorageConstants.FIRST_STEP_CLEANED_DATA_KEY,
            form.cleaned_data
        )

        return HttpResponseRedirect(self.get_success_url())


class BillingAddressView(FormView):
    form_class = BillForm
    template_name = 'signup/billing_address.html'
    success_url = '/confirm'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_id'] = UserService().get_from_session(
            self.request,
            SessionStorageConstants.COMPANY_ID
        )
        return context

    def get(self, request, *args, **kwargs):
        company = UserService().get_from_session(
            self.request,
            SessionStorageConstants.COMPANY_ID
        )
        if not company:
            raise Http404("No Company found")
        data = UserService().get_form_data_in_session(
            request,
            SessionStorageConstants.SECOND_STEP_KEY
        )
        if data:
            self.initial = data
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        UserService().set_form_data_in_session(
            self.request,
            SessionStorageConstants.SECOND_STEP_KEY,
            form.data
        )
        UserService().set_form_data_in_session(
            self.request,
            SessionStorageConstants.SECOND_STEP_CLEANED_DATA_KEY,
            form.cleaned_data
        )
        return HttpResponseRedirect(self.get_success_url())


class ConfirmVerifyView(TemplateView):
    template_name = 'signup/confirm.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form_0_data'] = UserService().get_form_data_in_session(
            self.request,
            SessionStorageConstants.FIRST_STEP_CLEANED_DATA_KEY
        )
        context['form_1_data'] = UserService().get_form_data_in_session(
            self.request,
            SessionStorageConstants.SECOND_STEP_CLEANED_DATA_KEY
        )
        company_id = UserService().get_from_session(
            self.request,
            SessionStorageConstants.COMPANY_ID
        )
        context['company'] = CompanyService().get_company(company_id)
        return context


class ConfirmView(TemplateView):
    template_name = 'signup/thank_you.html'

    def get(self, *args, **kwargs):
        session_cleared = UserService().check_session_cleared(self.request)
        if session_cleared:
            return HttpResponseRedirect('/')
        company_id = UserService().get_from_session(
            self.request,
            SessionStorageConstants.COMPANY_ID
        )
        company = CompanyService().get_company(company_id)
        user = UserService().create_user(
            self.request
        )
        address = ProfileService().create_address(
            self.request
        )
        if user and address:
            profile = ProfileService().create_profile(
                user=user,
                address=address,
                company=company
            )
            if profile:
                UserService().reset_all_session_data(self.request)
                return super().get(*args, **kwargs)

        raise HttpResponseServerError(
            "Internal Server Error. Please contact administrator")
