"""
Django User Adminsite
"""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from users.models import User
from profiles.models import Profile
from profiles.services import ProfileService
from companies.models import Company


class UserFilter(admin.SimpleListFilter):
    """
    They can filter and get Users
    """

    # right admin sidebar just above the filter options.
    title = _('User')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'user_type'

    def lookups(self, request, model_admin):
        if request.user.is_superuser:
            return (
                ("SuperUser", _("Super Users")),
                ("Staff", _("Staff Users")),
                ("User", _("Normal Users")),
            )
        else:
            return (
                ("Staff", _("Staff Users")),
                ("User", _("Normal Users")),
            )

    def queryset(self, request, queryset):
        if self.value() == 'SuperUser':
            return queryset.filter(is_superuser=True)
        elif self.value() == 'Staff':
            return queryset.filter(is_staff=True, is_superuser=False)
        elif self.value() == "User":
            return queryset.filter(is_superuser=False, is_staff=False)
        elif not self.value():
            return queryset
        else:
            queryset.none()


class CompanyFilter(admin.SimpleListFilter):
    """
    They can filter and get Users
    """

    # right admin sidebar just above the filter options.
    title = _('Company')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'company'

    def lookups(self, request, model_admin):
        company_list = []

        if request.user.is_superuser:
            for company in Company.objects.all():
                company_list.append((company.id, company.name))
        else:
            profile = ProfileService().get_profile(request.user)
            if profile:
                company_list.append(
                    (profile.company.id, profile.company.name)
                )
        return company_list

    def queryset(self, request, queryset):
        if self.value():
            try:
                profiles = Company.objects.get(
                    pk=int(self.value())).company_profiles.all()
                print(profiles)
                return User.objects.filter(
                    pk__in=profiles.values_list("user__id"))
            except (Company.DoesNotExist, Exception):
                pass

            return queryset.none()
        return queryset


class ProfileInline(admin.TabularInline):
    """
    Inline Module
    """
    model = Profile


class UserAdmin(admin.ModelAdmin):
    search_fields = [
        'email',
        'first_name',
        'last_name'
    ]

    list_display = [
        'email',
        'first_name',
        'last_name',
        'company',
        'billing_address'
    ]

    inlines = [
        ProfileInline,
    ]
    list_filter = [
        UserFilter,
        CompanyFilter,
    ]

    def get_profile(self, user):
        """
        Get Profile from User
        """
        return ProfileService().get_profile(user)

    def get_queryset(self, request):
        """
        Override
        """
        if request.user.is_superuser:
            # If User is super user, he will see all the users
            return User.objects.all()
        else:
            # If not, then he will only access the Company Users
            profile = self.get_profile(request.user)
            if profile:
                return profile.company.user_set.all()
        return User.objects.none()

    def billing_address(self, object):
        # Property method to get Billing Address
        profile = self.get_profile(object)
        if profile:
            return profile.billing_address

    def company(self, object):
        # Property Method to get Company Info
        profile = self.get_profile(object)
        if profile:
            return profile.company


admin.site.register(User, UserAdmin)  # Registering to adminsite
