"""
Company Model Admin
"""
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from companies.models import Company
from companies.constants import CompanyType
from profiles.services import ProfileService


class CompanyFilter(admin.SimpleListFilter):
    title = _("Company Types")
    parameter_name = 'company_type'

    def queryset(self, request, queryset):
        try:
            if self.value():
                value = int(self.value())
            else:
                value = None
        except Exception:
            value = -1

        if not value:
            return queryset
        elif value == CompanyType.PUBLIC:
            return queryset.filter(company_type=CompanyType.PUBLIC)
        elif value == CompanyType.LIMITED:
            return queryset.filter(company_type=CompanyType.LIMITED)
        elif value == CompanyType.LIMITED_PARTNERSHIP:
            return queryset.filter(
                company_type=CompanyType.LIMITED_PARTNERSHIP
            )
        elif value == CompanyType.NGO:
            return queryset.filter(company_type=CompanyType.NGO)
        elif value == CompanyType.STATUTORY:
            return queryset.filter(company_type=CompanyType.STATUTORY)
        elif value == CompanyType.HOLDING:
            return queryset.filter(company_type=CompanyType.HOLDING)
        elif value == CompanyType.CHARTERED:
            return queryset.filter(company_type=CompanyType.CHARTERED)
        elif value == CompanyType.ONEMAN:
            return queryset.filter(company_type=CompanyType.ONEMAN)
        elif value == CompanyType.UNLIMITED_PARTNERSHIP:
            return queryset.filter(
                company_type=CompanyType.UNLIMITED_PARTNERSHIP
            )
        else:
            return queryset.none()

    def lookups(self, request, model_admin):
        return (
            (CompanyType.PUBLIC, _('PUBLIC Companies')),
            (CompanyType.LIMITED, _('LIMITED Companies')),
            (CompanyType.LIMITED_PARTNERSHIP, _('LTD Partnership Companies')),
            (CompanyType.NGO, _('NGOs')),
            (CompanyType.STATUTORY, _('STATUTORY Companies')),
            (CompanyType.SUBSIDIARY, _('SUBSIDIARY Companies')),
            (CompanyType.CHARTERED, _('CHARTERED Companies')),
            (CompanyType.HOLDING, _('HOLDING Companies')),
            (CompanyType.ONEMAN, _('SINGLE OWNER Companies')),
            (CompanyType.UNLIMITED_PARTNERSHIP,
             _('UNLIMITED PARTNERSHIP Companies')),
        )


class CompanyAdmin(admin.ModelAdmin):
    """
    Company Admin Site (MODEL ADMIN CLASS)
    """
    list_display = [
        'name',
        'get_logo',
        'company_type'
    ]
    search_fields = ['name']

    list_filter = [
        CompanyFilter,
    ]

    def get_logo(self, object):
        """
        For displaying image in front end
        """
        return mark_safe('<img src="{}" height="42">'.format(object.logo.url))
    get_logo.short_description = 'Logo'

    def get_queryset(self, request):
        """
        Override
        """
        if request.user.is_superuser:
            return Company.objects.all()
        else:
            profile = self.get_profile(request.user)
            if profile:
                return [profile.company]

    def get_profile(self, user):
        """
        Get Profile Method
        """
        return ProfileService().get_profile(user)


admin.site.register(Company, CompanyAdmin)
